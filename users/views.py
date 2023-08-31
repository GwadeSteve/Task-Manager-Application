from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserLoginForm,CustomUserUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser

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
        form = CustomUserLoginForm(data=request.POST)
        print('formulaire recuperer')
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            print("Obtenu les donnees")
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                print("Success")
                return redirect('core:home')
            else:
                print("oopss")
                form.add_error('email', 'Invalid email or password.')
    else:
        print('massah')
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
