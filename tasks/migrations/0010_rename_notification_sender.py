# Generated by Django 4.2.9 on 2024-12-02 00:51

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0009_rename_created_at_notification_created_date'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Notification',
            new_name='Sender',
        ),
    ]
