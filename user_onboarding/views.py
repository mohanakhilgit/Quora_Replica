from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import RegisterForm


def signup_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login_user')
        else:
            messages.error(request, "Couldn't complete the registration! Please try again.")
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_user(request):
    if request.user.is_authenticated:
        messages.info(request, "User is already signed in!")
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, f"Welcome back {user.first_name}")
            return redirect('home')
        else:
            messages.error(request, "Username or Password is incorrect!")

    return render(request, 'login.html')


def logout_user(request):
    if not request.user.is_authenticated:
        messages.info(request, "Log in first!")
        return redirect('login_user')
    
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('login_user')
