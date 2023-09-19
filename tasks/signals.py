from django.db.models.signals import pre_save, post_delete,post_save
from django.dispatch import receiver
from .models import Task,Category

@receiver(pre_save, sender=Task)
def task_pre_save(sender, instance, **kwargs):
    try:
        old_task = Task.objects.get(pk=instance.pk)
    except Task.DoesNotExist:
        pass
    else:
        if instance.status != old_task.status:
            print("Attributes have changed!")
            pass
        else:
            # Store the original instance in the current instance's _original attribute
            instance._original = old_task

@receiver(post_save, sender=Task)
@receiver(post_save, sender=Category)
def model_changed(sender, instance, created, **kwargs):
    if not created:
        # Check if the _original attribute exists on the instance
        if hasattr(instance, '_original'):
            old_task = instance._original  # Get the original instance
            if instance.status != old_task.status:
                print("Attributes have changed!")

@receiver(post_delete, sender=Task)
@receiver(post_delete, sender=Category)
def model_deleted(sender, instance, **kwargs):
    # If an instance is deleted
    print(f"{sender.__name__} instance with ID {instance.id} was deleted.")

