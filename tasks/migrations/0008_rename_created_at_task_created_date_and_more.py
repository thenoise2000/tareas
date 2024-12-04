# Generated by Django 4.2.9 on 2024-12-02 00:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_remove_task_priority'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='created_at',
            new_name='created_date',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='due_date',
            new_name='expiration_date',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='updated_at',
            new_name='updated_date',
        ),
    ]
