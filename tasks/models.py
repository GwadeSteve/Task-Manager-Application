from django.db import models
from users.models import CustomUser
from datetime import datetime
from django.db.models import Count

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_task_count(self):
        return self.task_set.count()

    def get_completed_task_count(self):
        return self.task_set.filter(status='completed').count()
    
    def get_completion_count(self):
        Counts = {
            'completed':self.task_set.filter(status='completed').count(),
            'pending':self.task_set.filter(status='pending').count(),
            'late':self.task_set.filter(status='late').count(),
            'postponed':self.task_set.filter(status='postponed').count(),
        }
        return Counts

    def get_completed_tasks(self):
        return self.task_set.filter(status='completed')
    
    def get_pending_tasks(self):
        return self.task_set.filter(status='pending')
    
    def get_late_tasks(self):
        return self.task_set.filter(status='late')
    
    def get_postponed_tasks(self):
        return self.task_set.filter(status='postponed')

    def get_upcoming_due_tasks(self):
        return self.task_set.filter(status='pending', due_date__gte=datetime.today())

    def get_overdue_tasks(self):
        return self.task_set.filter(status='pending', due_date__lt=datetime.today())

    def get_task_priority_stats(self):
        return self.task_set.values('priority').annotate(count=Count('priority'))

    def get_latest_task(self):
        return self.task_set.latest('date_creation')

class Task(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('pending', 'Pending'),
        ('postponed', 'Postponed'),
        ('late','Late'),
    ]
    PRIORITY_CHOICES = [
        ('high', 'High Priority'),
        ('medium', 'Medium Priority'),
        ('low', 'Low Priority'),
    ]

    title = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    date_creation = models.DateField(auto_now_add=True)
    time_creation = models.TimeField(auto_now_add=True)
    due_date = models.DateField()
    due_time = models.TimeField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    attachments = models.FileField(upload_to='attachments/', blank=True, null=True)
    reminders = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
    
    def is_overdue(self):
        now = datetime.now()
        due_datetime = datetime.combine(self.due_date, self.due_time)
        return now > due_datetime

    def days_until_due(self):
        now = datetime.now()
        due_datetime = datetime.combine(self.due_date, self.due_time)
        timedelta = due_datetime - now
        return timedelta.days if timedelta.days >= 0 else 0

    def is_today_due(self):
        now = datetime.now()
        return self.due_date == now.date()

    def get_related_tasks(self):
        return Task.objects.filter(category=self.category)

    def get_attachment_count(self):
        return self.attachments.count()
