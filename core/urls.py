from django.urls import path
from . import views

urlpatterns = [
    path('loading/', views.loading_view, name='loading'),
    path('', views.home_view, name='home'),
]

