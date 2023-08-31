from django.shortcuts import render, redirect
from .models import Category, Task
from .forms import CategoryForm, TaskForm
from django.contrib import messages
from users.models import CustomUser

def create_category_view(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, 'Category created successfully.')
            return redirect('tasks:task-list')
    else:
        form = CategoryForm()
    return render(request, 'tasks/create_category.html', {'form': form})

def create_task_view(request):
    user = request.user
    default_categories = Category.objects.filter(name__in=['Work', 'School', 'Sports', 'Diet'])
    user_categories = Category.objects.filter(user=user)
    all_categories = default_categories | user_categories

    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        form.fields['category'].queryset = all_categories  # Limit category choices to user's categories
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task created successfully.')
            return redirect('core:home')
    else:
        form = TaskForm()
        form.fields['category'].queryset = all_categories  # Limit category choices to user's categories
    
    return render(request, 'tasks/create_task.html', {'form': form})

def task_list_view(request):
    return render(request,'tasks/task_list.html')

def task_category_view(request):
    return render(request,'tasks/task_category.html')
