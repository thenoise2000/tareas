from django.db import models
from django.contrib.auth.models import User
# Create your models here.

NOTIFICATION_TYPE = (
    ('Start', 'Start'), 
    ('End', 'End'), 
)

class Task(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, null = True)
    email = models.EmailField(max_length=255, null= True, blank = True)
    description = models.TextField(max_length=255, null= True, blank = True)    
    expiration_date = models.DateField()
    task_done = models.BooleanField(default = False) 
    message_send = models.BooleanField(default = False)

    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True)


    def __str__(self) -> str:
        return self.title  


class Sender(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    task = models.ForeignKey(Task, on_delete = models.CASCADE)
    type = models.CharField(max_length = 10, choices = NOTIFICATION_TYPE)
    created_date = models.DateTimeField(auto_now_add = True)

    def __str__(self) -> str:
        return self.task.title
    
    def full_message(self):
        if self.type == 'Start':
            return f"This {self.task.title} start today"
        return f"This task was expirated"