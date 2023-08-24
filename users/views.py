from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserLoginForm,CustomUserUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(request, username=user.email, password=form.cleaned_data['password1'])
            login(request, user)
            return redirect('tasks:task-list')  # Redirect to task list page
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.') #Display error message
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            email_or_phone = form.cleaned_data['email_or_phone']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email_or_phone, password=password)
            if user is not None:
                login(request, user)
                return redirect('tasks:task-list')  # Redirect to task list page
            else:
                messages.error(request, 'Login failed. Please check your email/phone and password.') #Error message
    else:
        form = CustomUserLoginForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('users:login') 

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile page or wherever you want
    else:
        form = CustomUserUpdateForm(instance=request.user)
    return render(request, 'users/update_profile.html', {'form': form})
