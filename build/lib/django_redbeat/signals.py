from django.dispatch import receiver
from django_redbeat.models import PeriodicTasksEntry
from django.db.models.signals import post_delete, post_save, pre_delete, pre_save
from redbeat import RedBeatSchedulerEntry as Entry


@receiver(post_save, sender=PeriodicTasksEntry)
def handle_periodic_task_admin(sender, instance, created, **kwargs):
    entry = instance.get_entry()
    if instance.enabled == False:
        # DISABLED THE TASK
        instance.delete_periodic_task()
    elif instance.enabled == True and entry is None:
        # ENABLED THE TASK
        instance.add_periodic_task()
        #entry.reschedule(instance.schedule)


"""
Signal to delete celery-redbeat  periodic tasks from django admin
"""
@receiver(pre_delete, sender=PeriodicTasksEntry)
def delete_periodic_task_entry_admin(sender, instance, using, **kwargs):
    entry = None
    try:
        entry = instance.get_entry()
    except Exception:
        pass
    if entry is not None:
        instance.delete_periodic_task()


@receiver(pre_save, sender=PeriodicTasksEntry)
def update_schedule(sender, instance, **kwargs):
    try:
        obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        print('Perioidc Task is new!')
        # Object is new, so field hasn't technically changed
    else:
        if not obj.schedule == instance.schedule : # TODO TEST THIS PROPERLY !!
              # Schedule field has changed
              instance.update_task_schedule()