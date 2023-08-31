from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('create-category/', views.create_category_view, name='create-category'),
    path('create-task/', views.create_task_view, name='create-task'),
    path('task-list/',views.task_list_view, name='task-list'),
    path('task-category/',views.task_category_view, name='task-category'),
    #path('task/<int:task_id>/', views.task_detail_view, name='task-detail'),
    #ath('category/<int:category_id>/', views.category_detail_view, name='category-detail'),
    #path('edit-task/<int:task_id>/', views.edit_task_view, name='edit-task'),
    #path('edit-category/<int:category_id>/', views.edit_category_view, name='edit-category'),
    #path('delete-task/<int:task_id>/', views.delete_task_view, name='delete-task'),
    #path('delete-category/<int:category_id>/', views.delete_category_view, name='delete-category'),
]
