from django.db.models import ExpressionWrapper, F, FloatField,Case, IntegerField,When, Value
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
from django.core.serializers import serialize
from django.db.models import Q
from datetime import datetime
import json
from django.db.models import Count
from django.db.models.functions import TruncDate

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
    #-Get all taska dn categories for the currently logged in user
    categories = Category.objects.filter(user=request.user)
    tasks = Task.objects.filter(user=request.user)

    #Category with most tasks
    Cat_dict = { category.name: category.get_task_count() for category in categories}
    Cat_with_most_tasks = {key: val for key, val in sorted(Cat_dict.items(), key = lambda ele: ele[1], reverse = True)}
    Cat_max_val = max(Cat_with_most_tasks.values())
    Cat_max_key = max(Cat_with_most_tasks,key=Cat_with_most_tasks.get)
    category_with_most_tasks = categories.get(name=Cat_max_key)
    cat_most_id = category_with_most_tasks.id

    #Category and task counts
    category_count = categories.count()
    task_count = tasks.count()

    #Completion counts
    completed_counts = Task.objects.filter(user=request.user, status='completed').count()
    pending_counts = Task.objects.filter(user=request.user, status='pending').count()
    postponed_counts = Task.objects.filter(user=request.user, status='postponed').count()
    late_counts = Task.objects.filter(user=request.user, status='late').count()

    # Fetch daily_completed_tasks_data
    daily_completed_tasks_data = Task.objects.filter(
        status='completed',
        user=request.user
    ).annotate(
        completion_date=TruncDate('due_date')
    ).values('completion_date').annotate(count=Count('id'))
    daily_completed_tasks_data = list(daily_completed_tasks_data)
    # Convert date objects to strings
    for entry in daily_completed_tasks_data:
        entry['completion_date'] = entry['completion_date'].strftime('%Y-%m-%d')
    # Convert the data to a JSON string
    daily_completed_tasks_data_json = json.dumps(daily_completed_tasks_data)
    print(daily_completed_tasks_data_json)

   # Calculate task status distribution
    task_status_distribution = Task.objects.filter(user=request.user).values('status').annotate(count=Count('status'))
    task_status_distribution_data = [{'status': item['status'], 'count': item['count']} for item in task_status_distribution]
    task_status_distribution_json = json.dumps(task_status_distribution_data)

    #Task Priority Distribution Bar Chart:
    priority_distribution = Task.objects.filter(user=request.user).values('priority').annotate(count=Count('id'))
    priority_distribution_json = json.dumps(list(priority_distribution))

    #Category-wise Completion Rate Radar Chart:
    category_distribution_data = Category.objects.annotate(task_count=Count('task')).values('name', 'task_count')
    # Convert the QuerySet to a list of dictionaries
    category_distribution_data = list(category_distribution_data)
    # Convert the data to a JSON string
    category_distribution_json = json.dumps(category_distribution_data)

    #Task Overdue Status Bar Chart:
    task_overdue_data = Task.objects.filter(status='overdue').values('status').annotate(count=Count('id'))
    task_overdue_data = list(task_overdue_data)
    task_overdue_json = json.dumps(task_overdue_data)

    #Task Completion Rate Histogram
    task_completion_rates = Task.objects.filter(user=request.user).annotate(
        completion_rate=ExpressionWrapper(
            Count('id', filter=F('status') == 'completed') * 100.0 / Count('id'), 
            output_field=FloatField()
        )
    ).values('completion_rate')

    context = {
        'category_count': category_count,
        'task_count': task_count,
        'completed_counts': completed_counts,
        'pending_counts': pending_counts,
        'postponed_counts': postponed_counts,
        'late_counts': late_counts,
        'Category_with_most_tasks_name': Cat_max_key,
        'Category_with_most_tasks_value': Cat_max_val,
        'cat_most_id': cat_most_id,
        'daily_completed_tasks': daily_completed_tasks_data_json,
        'task_status_distribution': task_status_distribution_json,
        'priority_distribution': priority_distribution_json,
        'category_distribution_json':category_distribution_json,
        'categories': categories,
        'task_overdue_json': task_overdue_json,
        'task_completion_rates': task_completion_rates,
    }

    return render(request, 'tasks/stats.html', context)

def completed_tasks(request):
    tasks = Task.objects.filter(status='completed')
    count = True if tasks.count() else False
    return render(request,'tasks/tasks.html',{'tasks':tasks,'count': count, 'type': 'Completed',})

def postponed_tasks(request):
    tasks = Task.objects.filter(status='postponed')
    count = True if tasks.count() else False
    return render(request,'tasks/tasks.html',{'tasks':tasks,'count': count, 'type': 'Postponed',})

def late_tasks(request):
    tasks = Task.objects.filter(status='late')
    count = True if tasks.count() else False
    return render(request,'tasks/tasks.html',{'tasks':tasks,'count': count, 'type': 'Late',})

def pending_tasks(request):
    tasks = Task.objects.filter(status='pending')
    count = True if tasks.count() else False
    return render(request,'tasks/tasks.html',{'tasks':tasks,'count': count, 'type': 'Pending',})

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


