from django import forms
from .models import Category, Task
from users.models import CustomUser
from django.core.exceptions import ValidationError
from datetime import datetime

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']


# Define a custom validation function for the due date
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['category', 'title', 'description', 'due_date', 'due_time', 'status', 'priority', 'attachments', 'reminders']
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the 'user' parameter
        super(TaskForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields['category'].queryset = Category.objects.filter(user=user)

    def clean_due_date(self):
        due_date = self.cleaned_data['due_date']
        today = datetime.now().date()

        # Check if the due date is in the past
        if due_date < today:
            raise ValidationError('Due date cannot be in the past.')

        return due_date

    def clean_due_time(self):
        due_datetime = datetime.combine(self.cleaned_data['due_date'], self.cleaned_data['due_time'])
        due_time = self.cleaned_data['due_time']
        now = datetime.now()
        # Check if the due time is in the past for the current day
        if due_datetime < now:
            raise ValidationError('Due time cannot be in the past.')
        return due_time

    def clean_reminder_datetime(self):
        reminder_datetime = self.cleaned_data['reminders']
        due_datetime = datetime.combine(self.cleaned_data['due_date'], self.cleaned_data['due_time'])

        # Check if the reminder datetime is in the future and after the due datetime
        if reminder_datetime <= due_datetime:
            raise ValidationError('Reminder datetime must be in the future and after the due datetime.')

        return reminder_datetime

    reminders = forms.DateTimeField(
        required=False,
        help_text='Enter the reminder datetime in the format YYYY-MM-DD HH:MM (e.g., 2023-09-13 08:00).',
        widget=forms.DateTimeInput(attrs={'placeholder': 'YYYY-MM-DD HH:MM'}),
    )

        

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


