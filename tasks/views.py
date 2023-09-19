from django.shortcuts import render, redirect,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Category, Task
from .forms import CategoryForm, TaskForm,EditTaskForm,EditCategoryForm
from django.contrib import messages
from users.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskSerializer,CategorySerializer
from django.db.models import Q

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
            return redirect('tasks:task-list')
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
            return redirect('tasks:task-list')
    else:
        form = EditCategoryForm(instance=category)

    return render(request,'tasks/edit_category.html',{'form':form,'category':category})   


@login_required
def mark_task_completed(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    old_status = task.status
    task.status = 'completed'
    task.save()
    return JsonResponse({'message': 'Task marked as completed successfully'})

@login_required
def mark_task_postponed(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    old_status = task.status 
    task.status = 'postponed'
    task.save()
    return JsonResponse({'message': 'Task marked as postponed successfully'})

@login_required
def check_task_status(request, task_id):
    task = get_object_or_404(Task,id=task_id, user = request.user)
    task_status = task.status
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
            return redirect('tasks:task-list')
    else:
        form = CategoryForm()
    return render(request, 'tasks/create_category.html', {'form': form})

@login_required
def create_task_view(request):
    user = request.user
    user_categories = Category.objects.filter(user=user)
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, user=user)
        if form.is_valid():
            category_name = form.cleaned_data.get('category')  # Get category name
            category = get_object_or_404(Category, user=user, name=category_name)  # Filter by user and category name
            task = form.save(commit=False)
            task.user = user
            task.category = category
            task.save()
            messages.success(request, 'Task created successfully.')
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

@login_required
def search(request):
    query = request.GET.get('q', '')
    task_results = Task.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query),
        user=request.user
    )
    category_results = Category.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query),
        user=request.user
    )
    Count_task = task_results.count()
    Count_category = category_results.count()
    return render(request, 'tasks/task_search.html', {
        'task_results': task_results, 
        'category_results': category_results, 
        'query': query,
        'Count_task': Count_task,
        'Count_category': Count_category,
        'Count' : Count_category+Count_task,
        }
    )
    

@csrf_exempt
@api_view(['GET'])
def get_updates(request):
    tasks = Task.objects.filter(user=request.user)
    categories = Category.objects.filter(user=request.user) 
    task_serializer = TaskSerializer(tasks, many=True)
    category_serializer = CategorySerializer(categories, many=True)
    data = {
        'tasks': task_serializer.data,
        'categories': category_serializer.data,
    }
    return Response(request.data)

