# Generated by Django 4.1.2 on 2022-10-23 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PeriodicTasksEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(blank=True, max_length=255, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('task', models.CharField(blank=True, max_length=255, null=True)),
                ('enabled', models.BooleanField(default=True)),
                ('schedule', models.IntegerField(default=10, help_text='The schedule in seconds.')),
                ('args', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Periodic Tasks Entry',
                'verbose_name_plural': 'Periodic Tasks Entries',
            },
        ),
    ]
