import json
from celery import Celery
from django.db import models
from redbeat import RedBeatSchedulerEntry as Entry
from celery.schedules import schedule
from celery import current_app
# Create your models here.
class PeriodicTasksEntry(models.Model):

    key = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    task = models.CharField(max_length=255, null=True, blank=True)
    enabled = models.BooleanField(default=True)
    schedule = models.IntegerField(default=10, help_text="The schedule in seconds.")
    args = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        self.key = self.add_periodic_task(args_list=self.get_args())
        instance = super(PeriodicTasksEntry, self).save(force_insert, force_update, *args, **kwargs)
        return instance

    def get_args(self):
        return json.loads(str(self.args))

    def get_entry(self):
        try:
            entry = Entry.from_key(self.key, app=current_app())
            return entry
        except Exception as e:
            return None

    def add_periodic_task(self, args_list, *args, **kwargs):
        try:
            # TASK ALREADY EXISTS IN REDIS
            entry = Entry.from_key(key=self.key)
            return entry.key
        except Exception as e:
            # TASK DOESNT EXIST IN REDIS
            entry = Entry(name=self.name, task=self.task, args=args_list, schedule=self.schedule, app=current_app)
            entry.save()
            self.key = entry.key
            return self.key

    def delete_periodic_task(self):
        entry = self.get_entry()
        if entry:
            entry.delete()
    
    def update_schedule(self, *args, **kwargs):
        entry = Entry.from_key(self.key, app=current_app())
        entry.schedule = schedule(run_every=self.schedule)
        entry.save()

    class Meta:
        verbose_name = 'Periodic Tasks Entry'
        verbose_name_plural = 'Periodic Tasks Entries'
