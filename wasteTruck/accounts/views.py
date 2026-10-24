from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, AdminUserCreationForm, AdminUserEditForm, DriverDetailsForm
from .decorators import role_required
from .models import User
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db import transaction
from truck.models import Driver, Truck, CollectionAssignment, Activity
from django.db.models import Count, Q

# Create your views here.


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username = username, 
            password = password
        )

        if user is not None:
            login(request, user)
            if user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'staff':
                return redirect('staff_dashboard')
            elif user.role == 'driver':
                return redirect('driver_dashboard')

        else:
            messages.error(request, "Invalid username or password")

    return render(request,'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@role_required('admin')
def admin_dashboard(request):
    users = User.objects.all()

    context = {
        'total_users': users.count(),
        'total_staff': users.filter(role='staff').count(),
        'total_drivers': users.filter(role='driver').count(),
        'total_admins': users.filter(role='admin').count(),
        'recent_users': users.order_by('-date_joined')[:5],
    }

    return render(request, 'admin_dashboard.html', context)


@login_required
@role_required('admin')
def manage_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        role = request.POST.get('role')

        if role not in ['staff', 'driver']:
            messages.error(request, 'Invalid role selected.')
            return redirect('manage_user')

        try:
            selected_user = User.objects.get(id=user_id)
        except (User.DoesNotExist, ValueError, TypeError):
            messages.error(request, 'User not found.')
            return redirect('manage_user')

        if selected_user.role == 'admin' or selected_user.is_superuser:
            messages.error(
                request,
                'Admin roles cannot be changed here.'
            )
            return redirect('manage_user')

        if selected_user.role == role:
            messages.info(
                request,
                f'{selected_user.username} already has this role.'
            )
            return redirect('manage_user')

        if role == 'driver':
            messages.info(
                request,
                'Please complete the driver details before saving the role.'
            )
            return redirect('user_edit', pk=selected_user.pk)

        selected_user.role = 'staff'
        selected_user.save(update_fields=['role'])

        messages.success(
            request,
            f'{selected_user.username} role updated to Staff.'
        )
        return redirect('manage_user')

    users = User.objects.all().order_by('username')
    return render(request, 'manage_user.html', {'users': users})



@login_required
@role_required('staff')
def staff_dashboard(request):
    today = timezone.localdate()

    # Truck statistics
    trucks = Truck.objects.all().order_by('truck_number')
    total_trucks = trucks.count()
    active_trucks = trucks.filter(status='active').count()

    # Driver statistics
    drivers = Driver.objects.select_related('user').order_by('full_name')
    total_drivers = drivers.count()
    active_drivers = drivers.filter(status='active').count()

    # Collection statistics
    assignments = CollectionAssignment.objects.select_related(
        'driver', 'truck'
    )

    todays_collections = assignments.filter(scheduled_date=today).count()
    total_assignments = assignments.count()
    completed_collections = assignments.filter(
        status='completed'
    ).count()

    pending_collections = assignments.filter(
        status='assigned'
    ).count()

    in_progress_collections = assignments.filter(
        status='in_progress'
    ).count()

    completion_percent = (
        round(completed_collections / total_assignments * 100)
        if total_assignments else 0
    )

    recent_activities = Activity.objects.order_by('-created_at')[:5]

    context = {
        'recent_activities': recent_activities,
        'total_trucks': total_trucks,
        'active_trucks': active_trucks,
        'total_drivers': total_drivers,
        'active_drivers': active_drivers,
        'todays_collections': todays_collections,
        'total_assignments': total_assignments,
        'completed_collections': completed_collections,
        'pending_collections': pending_collections,
        'in_progress_collections': in_progress_collections,
        'completion_percent': completion_percent,
        'trucks': trucks,
        'drivers': drivers,
    }

    return render(request, 'staff_dashboard.html', context)


@login_required
@role_required('driver')
def driver_dashboard(request):
    return render(request, "driver_dashboard.html")


@login_required
@role_required('admin')
def user_create(request):
    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST)
        driver_form = DriverDetailsForm(request.POST)

        if form.is_valid():
            role = form.cleaned_data['role']

            if role == 'driver' and not driver_form.is_valid():
                return render(request, 'user_form.html', {
                    'form': form,
                    'driver_form': driver_form,
                    'title': 'Create User Account',
                })

            try:
                with transaction.atomic():
                    user = form.save(commit=False)
                    user.role = role
                    user.save()

                    if role == 'driver':
                        driver = driver_form.save(commit=False)
                        driver.user = user
                        driver.save()

                messages.success(
                    request,
                    f'{user.username} account created successfully.'
                )
                return redirect('manage_user')

            except Exception as e:
                messages.error(
                    request,
                    'Could not create the account. '
                    'Check that the phone number and licence number '
                    'are not already registered.'
                )
    else:
        form = AdminUserCreationForm()
        driver_form = DriverDetailsForm()

    return render(request, 'user_form.html', {
        'form': form,
        'driver_form': driver_form,
        'title': 'Create User Account',
    })


@login_required
@role_required('admin')
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)

    if user.role == 'admin' or user.is_superuser:
        messages.error(request, 'Admin accounts are protected.')
        return redirect('manage_user')

    driver_instance = Driver.objects.filter(user=user).first()

    if request.method == 'POST':
        form = AdminUserEditForm(request.POST, instance=user)
        driver_form = DriverDetailsForm(
            request.POST,
            instance=driver_instance
        )

        if form.is_valid():
            role = form.cleaned_data['role']

            if role == 'driver' and not driver_form.is_valid():
                return render(request, 'user_form.html', {
                    'form': form,
                    'driver_form': driver_form,
                    'title': 'Edit User Account',
                })

            try:
                with transaction.atomic():
                    updated_user = form.save(commit=False)
                    updated_user.role = role
                    updated_user.save()

                    if role == 'driver':
                        driver = driver_form.save(commit=False)
                        driver.user = updated_user
                        driver.save()

                messages.success(
                    request,
                    f'{updated_user.username} account updated successfully.'
                )
                return redirect('manage_user')

            except Exception:
                messages.error(
                    request,
                    'Could not update the account. Check for duplicate '
                    'phone or licence numbers.'
                )
    else:
        form = AdminUserEditForm(instance=user)
        driver_form = DriverDetailsForm(instance=driver_instance)

    return render(request, 'user_form.html', {
        'form': form,
        'driver_form': driver_form,
        'title': 'Edit User Account',
    })



@login_required
@role_required('admin')
@require_POST
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)

    if user.role == 'admin' or user.is_superuser:
        messages.error(request, 'Admin accounts cannot be deleted here.')
        return redirect('manage_user')

    username = user.username
    user.delete()

    messages.success(
        request,
        f'{username} account deleted successfully.'
    )
    return redirect('manage_user')
