import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestor_tareas.settings')  

app = Celery('gestor_tareas')  
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()