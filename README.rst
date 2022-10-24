==============
Django RedBeat
==============

django-redbeat is an app based on celery-redbeat with model based celery periodic tasks.

Quick start
-----------

1. Add "django_redbeat" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django_redbeat',
    ]


2. Run ``python manage.py migrate`` to create the PeriodicTaskeEntry model.

3. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a periodic task (you'll need the Admin app enabled).

4. Visit http://127.0.0.1:8000/admin/django_redbeat/periodictasksentry/ to add periodic task.
5. Sample code to use::

     from django_redbeat import PeriodicTaskEntry

     task = PeriodicTasksEntry.objects.create(
        name="The verbose name of the task",
        task="yourapp.tasks.task_name",
        args=[arg1, arg2,],
        schedule=10# the schedule in seconds
     )