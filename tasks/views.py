from django.shortcuts import render, redirect,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Category, Task
from .forms import CategoryForm, TaskForm,EditTaskForm,EditCategoryForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskSerializer, CategoryWithCountsSerializer
from django.db.models import Q
from datetime import datetime
import json

#Creating tasks and categories 

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
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task created successfully.')
            return redirect('tasks:task-list')

    else:
        form = TaskForm(user=request.user)

    return render(request, 'tasks/create_task.html', {'form': form})


#Details

@login_required
def task_detail_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    return render(request, 'tasks/task_detail.html', {'task': task})

@login_required
def category_detail_view(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    completedTasks = category.get__counts()['completed']
    pendingTasks = category.get__counts()['pending']
    lateTasks = category.get__counts()['late']
    postponedTasks = category.get__counts()['postponed']
    context = {
        'category': category,
        'completed_num': completedTasks,
        'pending_num' : pendingTasks,
        'late_num': lateTasks,
        'postponed_num': postponedTasks,
    }
    return render(request, 'tasks/category_details.html',context)


#Edit Tasks and Categories
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


#Changing tasks statuses
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


#delete tasks and categories
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


#Task/Category list views
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


#Calendar
@login_required
def calendar(request):
    tasks = Task.objects.filter(user=request.user)
    event_colors = {
        'completed': '#379C2F',
        'pending': 'rgba(92, 182, 249, 1)',
        'late': 'rgb(251, 118, 118)',
        'postponed': 'rgba(253, 158, 46, 1)',
    }
    events = []
    for task in tasks:
        start_datetime = datetime(
            year=task.date_creation.year,
            month=task.date_creation.month,
            day=task.date_creation.day,
            hour=task.time_creation.hour,
            minute=task.time_creation.minute,
        )
        due_datetime = datetime(
            year=task.due_date.year,
            month=task.due_date.month,
            day=task.due_date.day,
            hour=task.due_time.hour,
            minute=task.due_time.minute,
        )
        event = {
            'id': task.id,  # Unique identifier for the event
            'title': task.title,
            'status': task.status,
            'color': event_colors.get(task.status, ''),  # Set color based on status
            'start': start_datetime.strftime('%Y-%m-%dT%H:%M:%S'),  # Use task creation datetime as start
            'end': due_datetime.strftime('%Y-%m-%dT%H:%M:%S'),  
            'allDay': False,  # Events span a specific time range
            'task_id': task.id,  # Store task ID for eventClick
        }
        events.append(event)

    return render(request, 'tasks/calendar.html', {'events': json.dumps(events)})


#Stats
@login_required
def stats(request):
    return render(request,'tasks/stats.html')


#Search functionality
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


#API
#Sending updates to frontend  
@csrf_exempt
@api_view(['GET'])
def get_updates(request):
    tasks = Task.objects.filter(user=request.user)
    categories = Category.objects.filter(user=request.user) 
    task_serializer = TaskSerializer(tasks, many=True)
    category_serializer = CategoryWithCountsSerializer(categories, many=True)  # Use the new serializer
    data = {
        'tasks': task_serializer.data,
        'categories': category_serializer.data,
    }
    return Response(data)


