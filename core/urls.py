from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.loading_view, name='loading'),
    path('home/', views.home_view, name='home'),
]

