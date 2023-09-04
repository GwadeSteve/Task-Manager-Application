from django.shortcuts import render,redirect
import time

# Create your views here.
def loading_view(request):
    return render(request,'core/loader.html')

def home_view(request):
    return render( request, 'core/home.html' )

def help(request):
    return render( request, 'core/help.html' )