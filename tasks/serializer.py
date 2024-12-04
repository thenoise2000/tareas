from rest_framework import serializers


from . models import Task
from django.conf import settings

class TaskSerializer(serializers.ModelSerializer):
    '''task serializer'''
    
    class Meta:
        model = Task
        fields = ('id','user', 'title', 'description', 'email', 'expiration_date', 'task_done')

    def get_user(self, obj):
        return obj.user.username if obj.user else None
    
    def to_representation(self, instance):
        '''for represent username'''
        data = super().to_representation(instance)
        data['user'] = self.get_user(instance)
        return data
    