# Generated by Django 4.0.4 on 2023-09-08 00:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('date_creation', models.DateField(auto_now_add=True)),
                ('time_creation', models.TimeField(auto_now_add=True)),
                ('due_date', models.DateField()),
                ('due_time', models.TimeField()),
                ('status', models.CharField(choices=[('completed', 'Completed'), ('pending', 'Pending'), ('postponed', 'Postponed'), ('late', 'Late')], default='pending', max_length=20)),
                ('priority', models.CharField(choices=[('high', 'High Priority'), ('medium', 'Medium Priority'), ('low', 'Low Priority')], default='medium', max_length=20)),
                ('attachments', models.FileField(blank=True, null=True, upload_to='attachments/')),
                ('reminders', models.DateTimeField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.category')),
            ],
        ),
    ]
