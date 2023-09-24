# serializers.py
from rest_framework import serializers
from .models import Task, Category

class TaskSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()  # Add this field to get the category name

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'date_creation', 'due_date', 'status', 'priority', 'category']

    def get_category(self, obj):
        return obj.category.name

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at']

class CategoryWithCountsSerializer(CategorySerializer):
    completed_task_count = serializers.SerializerMethodField()
    task_count = serializers.SerializerMethodField()

    class Meta(CategorySerializer.Meta):
        fields = CategorySerializer.Meta.fields + ['completed_task_count', 'task_count']

    def get_completed_task_count(self, obj):
        return obj.get_completed_task_count()

    def get_task_count(self, obj):
        return obj.get_task_count()
