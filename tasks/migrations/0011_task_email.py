# Generated by Django 4.2.9 on 2024-12-02 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0010_rename_notification_sender'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='email',
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
    ]