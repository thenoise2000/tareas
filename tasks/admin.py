from django.contrib import admin

# local import
from .models import Task, Sender
# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'expiration_date', 'task_done', 'message_send', 'created_date', 'updated_date']
    list_filter = ('expiration_date', 'created_date', 'task_done')    
    

@admin.register(Sender)
class SenderAdministrator(admin.ModelAdmin):
    list_display = ['task', 'user', 'type']