from django.contrib import admin
from .models import Task,Category
from users.models import CustomUser

# Register your models here.
admin.site.register(Task)
admin.site.register(CustomUser)
admin.site.register(Category)
