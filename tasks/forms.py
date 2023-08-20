from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'tags', 'attachments', 'reminders', 'status', 'estimated_time']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'reminders': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
