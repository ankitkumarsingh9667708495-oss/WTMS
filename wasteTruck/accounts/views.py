from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm
from .decorators import role_required
from .models import User
from django.utils import timezone

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

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Registration sucessfull! Please log in")
            return redirect('login')
        else:
            print(form.errors)

    else:
        form = RegistrationForm()

    return render(
        request, 'register.html', {'form':form}
    )


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



@role_required('admin')
def manage_user(request):

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        role = request.POST.get('role')

        # Validate the selected role
        if role not in ['staff', 'driver']:
            messages.error(request, 'Invalid role selected.')
            return redirect('manage_user')

        # Find the selected user
        try:
            selected_user = User.objects.get(id=user_id)
        except (User.DoesNotExist, ValueError, TypeError):
            messages.error(request, 'User not found.')
            return redirect('manage_user')

        # Prevent changing an existing admin's role
        if selected_user.role == 'admin':
            messages.error(
                request,
                'Admin roles cannot be changed here.'
            )
            return redirect('manage_user')

        # Save the new role
        selected_user.role = role
        selected_user.save(update_fields=['role'])

        messages.success(
            request,
            f'{selected_user.username} role updated successfully.'
        )

        return redirect('manage_user')

    # Display all users for GET requests
    users = User.objects.all().order_by('username')

    return render(request, 'manage_user.html', {'users': users})

@login_required
@role_required('staff')
def staff_dashboard(request):
    return render(request, 'staff_dashboard.html')

@login_required
@role_required('driver')
def driver_dashboard(request):
    return render(request, "driver_dashboard.html")