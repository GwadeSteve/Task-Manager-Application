# Generated by Django 4.0.4 on 2023-09-08 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_alter_category_description_alter_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(max_length=250),
        ),
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(max_length=50),
        ),
    ]
