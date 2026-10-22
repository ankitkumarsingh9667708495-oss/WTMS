from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from django.views.decorators.http import require_POST

from .models import Truck, Driver
from .forms import TruckForm, DriverForm


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
            form.save()
            messages.success(request, 'Truck registered successfully.')
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
            form.save()
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