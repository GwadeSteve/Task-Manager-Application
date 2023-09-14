# tasks/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Task, Category

class TaskConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.user = self.scope["user"]
        await self.channel_layer.group_add(
            f"user_{self.user.id}", self.channel_name
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f"user_{self.user.id}", self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data["action"]
        if action == "get_updates":
            await self.send_updates()

    async def send_updates(self):
        user_id = self.user.id
        tasks = Task.objects.filter(user_id=user_id)
        categories = Category.objects.filter(user_id=user_id)
        task_data = [{"id": task.id, "title": task.title, "status": task.status} for task in tasks]
        category_data = [{"id": category.id, "name": category.name} for category in categories]

        await self.send(json.dumps({"type": "update_data", "tasks": task_data, "categories": category_data}))
