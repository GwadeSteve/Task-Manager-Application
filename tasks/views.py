from django.shortcuts import render, redirect,get_object_or_404
from .models import Category, Task
from .forms import CategoryForm, TaskForm,EditTaskForm,EditCategoryForm
from django.contrib import messages
from users.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def task_detail_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    return render(request, 'tasks/task_detail.html', {'task': task})

@login_required
def category_detail_view(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    return render(request, 'tasks/category_details.html', {'category': category})

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
def edit_category_view(request,category_id):
    user = request.user
    category = get_object_or_404(Category,id=category_id,user=user)
    if request.method == 'POST':
        form = EditCategoryForm(instance=category , data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks:category-detail',category_id=category.id)
    else:
        form = EditCategoryForm(instance=category)

    return render(request,'tasks/edit_category.html',{'form':form,'category':category})   


@login_required
def mark_task_completed(request, task_id):
    task = get_object_or_404(Task, id=task_id,user=request.user)
    task.status = 'completed'
    task.save()
    return JsonResponse({'message': 'Task marked as completed successfully'})

@login_required
def mark_task_postponed(request, task_id):
    task = get_object_or_404(Task, id=task_id,user=request.user)
    task.status = 'postponed'
    task.save()
    return JsonResponse({'message': 'Task marked as postponed successfully'})

@login_required
def check_task_status(request, task_id):
    task = get_object_or_404(Task,id=task_id, user = request.user)
    task_status = task.status  # Replace with your actual attribute for task status
    return JsonResponse({'status': task_status})

@login_required
def delete_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':
        task.delete()
        return redirect('tasks:task-list')

    return render(request, 'tasks/delete_task.html', {'task': task})

@login_required
def delete_category_view(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)

    if request.method == 'POST':
        category.delete()
        return redirect('tasks:task-list')

    return render(request, 'tasks/delete_category.html', {'category':category})

@login_required
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

@login_required
def create_task_view(request):
    user = request.user
    user_categories = Category.objects.filter(user=user)
    if request.method == 'POST':
        form = TaskForm(user=user, data=request.POST, files=request.FILES)
        if form.is_valid():
            category_id = request.POST.get('category')
            category = get_object_or_404(Category, id=category_id, user=user)
            form.instance.category = category
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('tasks:task-list')
    else:
        form = TaskForm(user=user)
        form.fields['category'].queryset = user_categories
    
    return render(request, 'tasks/create_task.html', {'form': form})

@login_required
def task_list_view(request):
    categories = Category.objects.filter(user=request.user)
    tasks = Task.objects.filter(user=request.user)
    return render(request,'tasks/task_list.html',{'categories':categories,'tasks':tasks})

@login_required
def task_category_view(request):
    categories = Category.objects.filter(user=request.user)
    tasks = Task.objects.filter(user=request.user)
    return render(request,'tasks/task_category.html',{'categories':categories,'tasks':tasks,})

@login_required
def calendar(request):
    return render(request,'tasks/calendar.html')

@login_required
def stats(request):
    return render(request,'tasks/stats.html')
