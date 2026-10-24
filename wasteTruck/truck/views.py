from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from django.views.decorators.http import require_POST
from django.db import transaction, models
from .models import Truck, Driver, CollectionAssignment, Activity
from .forms import TruckForm, DriverForm, CollectionAssignmentForm
from django.utils import timezone


@login_required
@role_required('staff', 'admin')
def truck_list(request):
    trucks = Truck.objects.all().order_by('truck_number')

    # Search by truck number
    search_query = request.GET.get('search', '').strip()

    if search_query:
        trucks = trucks.filter(
            truck_number__icontains=search_query
        )

    # Filter by status
    status = request.GET.get('status', '')

    if status:
        trucks = trucks.filter(status=status)

    # Filter by fuel type
    fuel_type = request.GET.get('fuel_type', '')

    if fuel_type:
        trucks = trucks.filter(fuel_type=fuel_type)

    # Filter by compatible waste type
    waste_type = request.GET.get('waste_type', '')

    if waste_type:
        trucks = trucks.filter(
            compatible_waste_type=waste_type
        )

    context = {
        'trucks': trucks,
        'search_query': search_query,
        'selected_status': status,
        'selected_fuel_type': fuel_type,
        'selected_waste_type': waste_type,
        'status_choices': Truck.STATUS_CHOICES,
        'fuel_choices': Truck.FUEL_CHOICES,
        'waste_choices': Truck.WASTE_CHOICES,
    }

    return render(request, 'truck_list.html', context)




@login_required
@role_required('staff', 'admin')
def truck_create(request):
    if request.method == 'POST':
        form = TruckForm(request.POST)

        if form.is_valid():
            truck = form.save()

            Activity.objects.create(
                action='truck_added',
                description=(
                    f'Truck {truck.truck_number} was registered '
                    f'successfully.'
                )
            )

            messages.success(
                request,
                'Truck registered successfully.'
            )
            return redirect('truck_list')
    else:
        form = TruckForm()

    return render(request, 'truck_form.html', {
        'form': form,
        'title': 'Register New Truck'
    })

@login_required
@role_required('staff', 'admin')
def truck_edit(request, pk):
    truck = get_object_or_404(Truck, pk=pk)

    if request.method == 'POST':
        form = TruckForm(request.POST, instance=truck)

        if form.is_valid():
            form.save()
            messages.success(request, 'Truck details updated successfully.')
            return redirect('truck_list')

    else:
        form = TruckForm(instance=truck)

    return render(request, 'truck_form.html', {
        'form': form,
        'title': 'Edit Truck'
    })


@login_required
@role_required('staff', 'admin')
@require_POST
def truck_delete(request, pk):
    truck = get_object_or_404(Truck, pk=pk)
    truck_number = truck.truck_number

    truck.delete()

    messages.success(
        request,
        f'Truck {truck_number} deleted successfully.'
    )

    return redirect('truck_list')



@login_required
@role_required('staff', 'admin')
def driver_list(request):
    drivers = Driver.objects.all().order_by('full_name')

    return render(request, 'driver_list.html', {
        'drivers': drivers
    })



@login_required
@role_required('staff', 'admin')
def driver_create(request):
    if request.method == 'POST':
        form = DriverForm(request.POST)

        if form.is_valid():
            driver = form.save()

            Activity.objects.create(
                action='driver_added',
                description=(
                    f'Driver {driver.full_name} was registered '
                    f'successfully.'
                )
            )

            messages.success(
                request,
                'Driver registered successfully.'
            )
            return redirect('driver_list')
    else:
        form = DriverForm()

    return render(request, 'driver_form.html', {
        'form': form,
        'title': 'Register New Driver'
    })


@login_required
@role_required('staff', 'admin')
def driver_edit(request, pk):
    driver = get_object_or_404(Driver, pk=pk)

    if request.method == 'POST':
        form = DriverForm(request.POST, instance=driver)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Driver details updated successfully.'
            )
            return redirect('driver_list')
    else:
        form = DriverForm(instance=driver)

    return render(request, 'driver_form.html', {
        'form': form,
        'title': 'Edit Driver'
    })


@login_required
@role_required('staff', 'admin')
@require_POST
def driver_delete(request, pk):
    driver = get_object_or_404(Driver, pk=pk)
    driver_name = driver.full_name

    driver.delete()

    messages.success(
        request,
        f'Driver {driver_name} deleted successfully.'
    )

    return redirect('driver_list')


@login_required
@role_required('staff', 'admin')
def collection_assignment_create(request):
    if request.method == 'POST':
        form = CollectionAssignmentForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                # Lock the selected resources before rechecking availability.
                driver = Driver.objects.select_for_update().get(
                    pk=form.cleaned_data['driver'].pk
                )
                truck = Truck.objects.select_for_update().get(
                    pk=form.cleaned_data['truck'].pk
                )

                # Recheck driver availability inside the transaction.
                if driver.status != 'active':
                    form.add_error(
                        'driver',
                        'This driver is no longer active.'
                    )

                elif driver.license_expiry < timezone.localdate():
                    form.add_error(
                        'driver',
                        'This driver has an expired licence and cannot be assigned.'
                    )

                elif Truck.objects.filter(
                    assigned_driver=driver
                ).exists():
                    form.add_error(
                        'driver',
                        'This driver is already assigned to a truck.'
                    )

                elif CollectionAssignment.objects.filter(
                    driver=driver,
                    status__in=['assigned', 'in_progress']
                ).exists():
                    form.add_error(
                        'driver',
                        'This driver already has an ongoing collection.'
                    )

                # Recheck truck availability inside the transaction.
                if truck.status != 'active':
                    form.add_error(
                        'truck',
                        'This truck is no longer active.'
                    )

                elif truck.assigned_driver_id is not None:
                    form.add_error(
                        'truck',
                        'This truck is already assigned to a driver.'
                    )

                elif CollectionAssignment.objects.filter(
                    truck=truck,
                    status__in=['assigned', 'in_progress']
                ).exists():
                    form.add_error(
                        'truck',
                        'This truck already has an ongoing collection.'
                    )

                # Save only if both resources remain available.
                if not form.errors:
                    assignment = form.save(commit=False)
                    assignment.driver = driver
                    assignment.truck = truck
                    assignment.save()

                    truck.assigned_driver = driver
                    truck.save(update_fields=['assigned_driver'])

                    Activity.objects.create(
                        action='collection_assigned',
                        description=(
                            f'{driver.full_name} was assigned to '
                            f'route {assignment.route} using truck '
                            f'{truck.truck_number}.'
                        )
                    )

            if form.errors:
                messages.error(
                    request,
                    'The assignment could not be created. '
                    'Please check the errors below.'
                )
            else:
                messages.success(
                    request,
                    'Collection assignment created successfully.'
                )
                return redirect('collection_assignment_create')

    else:
        form = CollectionAssignmentForm()

    return render(
        request,
        'collection_assignment_form.html',
        {
            'form': form,
            'title': 'Create Collection Assignment',
        }
    )


@login_required
@role_required('staff', 'admin')
def collection_assignment_list(request):
    assignments = CollectionAssignment.objects.select_related(
        'driver',
        'truck'
    ).order_by('-scheduled_date', '-created_at')

    # Search by driver name, truck number, or route
    search_query = request.GET.get('search', '').strip()

    if search_query:
        assignments = assignments.filter(
            models.Q(driver__full_name__icontains=search_query) |
            models.Q(truck__truck_number__icontains=search_query) |
            models.Q(route__icontains=search_query)
        )

    # Filter by assignment status
    status = request.GET.get('status', '')

    if status:
        assignments = assignments.filter(status=status)

    context = {
        'assignments': assignments,
        'search_query': search_query,
        'selected_status': status,
        'status_choices': CollectionAssignment.STATUS_CHOICES,
    }

    return render(
        request,
        'collection_assignment_list.html',
        context
    )



@login_required
@role_required('staff', 'admin')
@require_POST
def collection_assignment_update_status(request, pk):
    with transaction.atomic():
        assignment = get_object_or_404(
            CollectionAssignment.objects.select_for_update()
            .select_related('truck', 'driver'),
            pk=pk
        )

        new_status = request.POST.get('status')

        allowed_transitions = {
            'assigned': ['in_progress'],
            'in_progress': ['completed'],
            'completed': [],
        }

        if new_status not in allowed_transitions.get(
            assignment.status, []
        ):
            messages.error(
                request,
                'Invalid assignment status change.'
            )
            return redirect('collection_assignment_list')

        # Update the collection status.
        assignment.status = new_status
        assignment.save(update_fields=['status'])

        # Release the truck when the collection is completed.
        if new_status == 'completed':
            truck = Truck.objects.select_for_update().get(
                pk=assignment.truck_id
            )

            other_active_assignments = (
                CollectionAssignment.objects.filter(
                    truck_id=assignment.truck_id,
                    status__in=['assigned', 'in_progress']
                ).exclude(pk=assignment.pk)
            )

            # Clear the driver only if this truck is still
            # assigned to the driver who completed this collection.
            if (
                not other_active_assignments.exists()
                and truck.assigned_driver_id == assignment.driver_id
            ):
                truck.assigned_driver = None
                truck.save(update_fields=['assigned_driver'])

                Activity.objects.create(
                    action='collection_completed',
                    description=(
                        f'{assignment.driver.full_name} completed the collection '
                        f'for route {assignment.route} using truck '
                        f'{truck.truck_number}.'
                    )
                )

        messages.success(
            request,
            f'Assignment status updated to '
            f'{assignment.get_status_display()}.'
        )

    return redirect('collection_assignment_list')
