from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserLoginForm,CustomUserUpdateForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from .models import CustomUser
from tasks.models import Category
import time

@never_cache
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user object
            # Authenticate the user and log them in
            user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            messages.success(request,'Registration succesfull.')
            for category_name in ['Work', 'Sports', 'Diet']:
                Category.objects.create(name=category_name, description=f"This is the default category created for you to manage your {category_name} tasks", user=user)
            login(request, user)
            return redirect('tasks:task-list')  # Redirect to task category page
        else:
            messages.error(request, 'Invalid registration, Checkout email and password')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@never_cache
def login_view(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                messages.success(request,'Logged in succesfully.')
                login(request, user)
                return redirect('tasks:task-list')
            else:
                messages.error(request, 'Invalid credentials, Please check email and password')
    else:
        form = CustomUserLoginForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('core:home')

@login_required
def profile(request):
    return render(request,'users/profile.html')

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
