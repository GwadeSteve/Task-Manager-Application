# Generated by Django 4.0.4 on 2023-09-24 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='reminders',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
