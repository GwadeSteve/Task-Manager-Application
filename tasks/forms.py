from django import forms
from .models import Category, Task
from users.models import CustomUser

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        
class TaskForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)
        
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'due_time', 'category', 'status', 'priority', 'attachments', 'reminders']

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
        fields = ['title', 'description', 'due_date', 'due_time', 'category', 'status', 'priority', 'attachments', 'reminders']

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

