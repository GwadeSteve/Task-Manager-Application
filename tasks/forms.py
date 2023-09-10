from django import forms
from .models import Category, Task
from users.models import CustomUser
from django.core.exceptions import ValidationError
from datetime import datetime

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']


def validate_due_date_time(value):
    # Get the current date and time
    now = datetime.now()

    # Check if the due date is in the past
    if value.date() < now.date():
        raise ValidationError('Due date cannot be in the past.')

    # Check if the due date is today and the due time is in the past
    if value.date() == now.date() and value.time() < now.time():
        raise ValidationError('Due time cannot be in the past.')
        
class TaskForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)

    #Validate the due date and time 
    due_date = forms.DateTimeField(validators=[validate_due_date_time])
        
    class Meta:
        model = Task
        fields = [ 'category','title', 'description', 'due_date', 'due_time', 'status', 'priority', 'attachments', 'reminders']

class EditCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

class EditTaskForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(EditTaskForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)

    class Meta:
        model = Task
        fields = ['category','title', 'description', 'due_date', 'due_time', 'status', 'priority', 'attachments', 'reminders']

class TaskFilterForm(forms.Form):
    STATUS_CHOICES = [
        ('', 'All'),
        ('completed', 'Completed'),
        ('pending', 'Pending'),
        ('postponed', 'Postponed'),
    ]
    PRIORITY_CHOICES = [
        ('', 'All'),
        ('high', 'High Priority'),
        ('medium', 'Medium Priority'),
        ('low', 'Low Priority'),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False)
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES, required=False)
    category = forms.ModelChoiceField(queryset=None, empty_label='All', required=False)

    def __init__(self, user, *args, **kwargs):
        super(TaskFilterForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)

