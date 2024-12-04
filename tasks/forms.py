from django import forms
from .models import Task


class TaskCreationForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required= False)
    class Meta:
        model = Task
        fields = ['title', 'description', 'email', 'expiration_date']
        widgets = {
                'expiration_date': forms.DateInput(attrs={'type': 'date'}),
        }


class TaskUpdateForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    class Meta:
        model = Task
        fields = ['title', 'description', 'email', 'expiration_date', 'task_done' ]
        widgets = {
            'expiration_date': forms.DateInput(attrs={'type': 'date'}),
        }