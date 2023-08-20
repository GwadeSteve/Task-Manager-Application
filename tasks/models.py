from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, validators=[MinLengthValidator(1)])
    description = models.TextField(validators=[MinLengthValidator(1)])
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=20, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])
    tags = models.ManyToManyField('Tag', blank=True)
    attachments = models.ManyToManyField('Attachment', blank=True)
    start_date = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    reminders = models.ManyToManyField('Reminder', blank=True)
    status = models.CharField(max_length=20, choices=[('in_progress', 'In Progress'), ('completed', 'Completed'), ('postponed', 'Postponed')])
    estimated_time = models.DurationField(null=True, blank=True)

    def __str__(self):
        return self.title

    def mark_completed(self):
        self.status = 'completed'
        self.save()

    def add_attachment(self, attachment):
        self.attachments.add(attachment)
        self.save()

    def add_reminder(self, reminder):
        self.reminders.add(reminder)
        self.save()

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Attachment(models.Model):
    file = models.FileField(upload_to='attachments/')

    def __str__(self):
        return self.file.name

class Reminder(models.Model):
    remind_at = models.DateTimeField()

    def __str__(self):
        return str(self.remind_at)
