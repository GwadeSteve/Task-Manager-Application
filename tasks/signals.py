from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Task,Category
from .utils import trigger_update

@receiver(post_save, sender=Task)
@receiver(post_delete, sender=Task)
def task_change_handler(sender, instance, **kwargs):
    # Trigger an update when a Task is created, updated, or deleted
    trigger_update(instance.user)

@receiver(post_save, sender=Category)
@receiver(post_delete, sender=Category)
def category_change_handler(sender, instance, **kwargs):
    # Trigger an update when a Category is created, updated, or deleted
    trigger_update(instance.user)
