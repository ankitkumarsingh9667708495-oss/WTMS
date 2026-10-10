from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm

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
            return redirect('dashboard')

        else:
            messages.error(request, "Invalid username or password")

    return render(request,'login.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

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