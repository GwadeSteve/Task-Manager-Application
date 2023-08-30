from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserLoginForm,CustomUserUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser

def Loader(request):
    return render(request, 'users/loading.html')

def HomeView(request):
    return render(request,'users/home.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user object
            # Authenticate the user and log them in
            user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            login(request, user)
            return redirect('core:home')  # Redirect to the home page after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Check if the email exists in the database
            if CustomUser.objects.filter(email=email).exists():
                user = authenticate(email=email, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('core:home')  # Redirect to home page after successful login
            else:
                form.add_error('username', 'This email does not exist.')
    else:
        form = CustomUserLoginForm()
    return render(request, 'users/login.html', {'form': form})



@login_required
def logout_view(request):
    logout(request)
    return redirect('core:home')

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
