import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from tasks.models import Task, Category
from tasks.signals import task_change_handler,category_change_handler  # Import your task_change_handler
from django.db.models.signals import post_save, post_delete
from .utils import trigger_update

class RealTimeUpdatesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        user = self.scope["user"]
        if user.is_authenticated:
            await self.send_all_data(user)  # Send all tasks and categories when the user connects
        # Register the user to the user-specific group
        await self.channel_layer.group_add(f"user_{user.id}", self.channel_name)

    async def disconnect(self, close_code):
        user = self.scope["user"]
        if user.is_authenticated:
            # Remove the user from the user-specific group when they disconnect
            await self.channel_layer.group_discard(f"user_{user.id}", self.channel_name)

    async def send_all_data(self, user):
        tasks = Task.objects.filter(user=user)
        categories = Category.objects.filter(user=user)
        tasks_data = [
            {
                'id': task.id,
                'status': task.status,
                'title': task.title,
                'priority': task.priority,
                'category': task.category.name,
                'date_creation': task.date_creation.strftime('%Y-%m-%d'),
                'due_date': task.due_date.strftime('%Y-%m-%d'),
            } for task in tasks
        ]
        categories_data = [
            {
                'id': category.id,
                'name': category.name,
                'description': category.description,
                'completed_tasks': category.get_completed_task_count(),
                'total_tasks': category.get_task_count(),
                'created_at': category.created_at.strftime('%Y-%m-%d %H:%M:%S')
            } for category in categories
        ]
        data = {
            'tasks': tasks_data,
            'categories': categories_data,
        }
        await self.send(json.dumps(data))

    async def send_updates(self, event):
        await self.send(event['data'])  # Send updates to the user

    # This is called when a task is created, updated, or deleted
    @staticmethod
    def task_change_handler(sender, instance, **kwargs):
        trigger_update(instance.user)

    @staticmethod
    def category_change_handler(sender, instance, **kwargs):
        trigger_update(instance.user)

# Connect signals to their handlers
post_save.connect(RealTimeUpdatesConsumer.task_change_handler, sender=Task)
post_delete.connect(RealTimeUpdatesConsumer.task_change_handler, sender=Task)
post_save.connect(RealTimeUpdatesConsumer.category_change_handler, sender=Category)
post_delete.connect(RealTimeUpdatesConsumer.category_change_handler, sender=Category)
