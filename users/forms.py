from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'phone_number', 'first_name', 'last_name', 'password1', 'password2')

class CustomUserLoginForm(forms.Form):
    email_or_phone = forms.CharField(label='Email or Phone Number')
    password = forms.CharField(widget=forms.PasswordInput)
