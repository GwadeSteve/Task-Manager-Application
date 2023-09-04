from django.shortcuts import render, redirect,get_object_or_404
from .models import Category, Task
from .forms import CategoryForm, TaskForm,EditTaskForm
from django.contrib import messages
from users.models import CustomUser
from django.contrib.auth.decorators import login_required

@login_required
def task_detail_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    return render(request, 'tasks/task_detail.html', {'task': task})

@login_required
def edit_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        form = EditTaskForm(request.user, request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks:task-detail', task_id=task.id)
    else:
        form = EditTaskForm(request.user, instance=task)

    return render(request, 'tasks/edit_task.html', {'form': form, 'task': task})

@login_required
def delete_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':
        task.delete()
        return redirect('tasks:task-list')

    return render(request, 'tasks/delete_task.html', {'task': task})

@login_required
def create_category_view(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, 'Category created successfully.')
            return redirect('tasks:task-category')
    else:
        form = CategoryForm()
    return render(request, 'tasks/create_category.html', {'form': form})

@login_required
def create_task_view(request):
    user = request.user
    default_categories = Category.objects.filter(name__in=['Work', 'School', 'Sports', 'Diet'])
    user_categories = Category.objects.filter(user=user)
    all_categories = default_categories | user_categories

    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, user=user)
        form.fields['category'].queryset = all_categories  # Limit category choices to user's categories
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task created successfully.')
            return redirect('tasks:task-list')
    else:
        form = TaskForm(user=request.user)
        form.fields['category'].queryset = all_categories  # Limit category choices to user's categories
    
    return render(request, 'tasks/create_task.html', {'form': form})

@login_required
def task_list_view(request):
    return render(request,'tasks/task_list.html')

@login_required
def task_category_view(request):
    return render(request,'tasks/task_category.html')

@login_required
def calendar(request):
    return render(request,'tasks/calendar.html')

@login_required
def stats(request):
    return render(request,'tasks/stats.html')
