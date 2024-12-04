from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.views.generic import View, ListView, DeleteView, DetailView
from django.contrib import messages
from django.urls import reverse_lazy
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import authenticate
from datetime import date
from django.shortcuts import render, HttpResponse
from .tasks import send_email_task
from django.views.generic import ListView

# local import
from .models import Task, Sender
from .forms import TaskCreationForm, TaskUpdateForm
from .serializer import TaskSerializer
# Create your views here.

######################### Template View ############################

class HomeView(ListView):
    model = Task
    template_name = 'index.html'
    context_object_name = 'tasks'
    paginate_by = 6  # Número de tareas por página

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Task.objects.filter(user=self.request.user).order_by('-created_date')
        return Task.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Aquí no es necesario crear un paginator manualmente, 
        # ya que ListView lo maneja automáticamente.
        return context


class FilterView(LoginRequiredMixin, ListView):
    '''Filter by category like completed, incompleted etc'''
    model = Task
    template_name = 'index.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        category = self.kwargs['category']
        if category == 'Done':
            return Task.objects.filter(user = self.request.user, task_done = True)
        elif category == 'Pending':
            return Task.objects.filter(user = self.request.user, task_done = False)
        elif category == 'created':
            return Task.objects.filter(user = self.request.user).order_by('-created_date')
        elif category == 'expiration_date':
            return Task.objects.filter(user = self.request.user).order_by('expiration_date')        
        else:
            return None


class TaskCreateView(LoginRequiredMixin, FormView):
    '''Create Task and must be an Authenticate user'''

    template_name = 'tasks/formAddTasks.html'
    form_class = TaskCreationForm
    success_url = reverse_lazy('index')
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user 
        instance.save() 

        # Enviar correo electrónico
        #subject = "Nueva tarea creada"
        #message = f"Se ha creado una nueva tarea: "
        #recipient_list = 'thenoise2000@gmail.com'
        #send_email_task.delay(subject, message, recipient_list)       

        messages.success(self.request, 'Task created successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Someting missing, please try again :(')
        return self.render_to_response(self.get_context_data(form=form))

    def handle_no_permission(self):
        messages.warning(self.request, 'You need to be logged in.')
        return redirect('login')
    
    def celerymail(request):
        send_email_task.delay(10)
        return HttpResponse('Email has been sent!!')

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    '''Delete a Task'''
    model = Task
    template_name = 'tasks/formDeleteTask.html'
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        try:
            task = Task.objects.get(pk =self.kwargs['id'])
            return task
        except:
            messages.warning(self.request, "Task doesn't exist!")
            return None
        
    def handle_no_permission(self):
        messages.warning(self.request, 'You need to be logged in.')
        return redirect('login')


class TaskDetailView(LoginRequiredMixin, DetailView):
    '''Single Task Detail view'''
    model = Task
    template_name = 'tasks/taskDetail.html'
    context_object_name = 'task'

class TaskUpdateView(LoginRequiredMixin, FormView):
    '''Update task and also upload multple image'''
    model = Task
    template_name = 'tasks/formUpdateTask.html'
    form_class = TaskUpdateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        task_id = self.kwargs.get('id')
        task = Task.objects.get(pk=task_id, user=self.request.user)
        kwargs['instance'] = task
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_id = self.kwargs.get('id')
        try:
            context['task'] = Task.objects.get(pk=task_id, user=self.request.user)
        except:
            pass
        return context
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        if instance.expiration_date > date.today() or instance.task_done == True:
            try:
                Sender.objects.filter(task=instance, type='End').delete() 
                instance.message_send = False
                instance.save()
            except:
                pass

        # Enviar correo electrónico
        #subject = "tarea modificada"
        #message = f"Se ha modificado una tarea: "
        #recipient_list = 'thenoise2000@gmail.com'
        #send_email_task.delay(subject, message, recipient_list) 
        
        instance.save()
        
        return redirect('task-details', pk=instance.id)

    def form_invalid(self, form):
        task_id = self.kwargs.get('task_id')
        task = Task.objects.get(pk=task_id, user=self.request.user)
        messages.error(self.request, 'Something Error :(')
        return render(self.request, self.template_name, {'form': form, 'task': task})
    
    def handle_no_permission(self):
        messages.warning(self.request, 'You need to be logged in.')
        return redirect('login')


class TaskSearchView(LoginRequiredMixin, View):
    '''Search by title of the task'''
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        title = request.GET.get('title', None)
        if title:
            tasks = Task.objects.filter(title__icontains=title, user = request.user)
            context = {'search': True, 'tasks': tasks}
            return render(request, self.template_name, context)
        else:
            redirect('index')

    def handle_no_permission(self):
        messages.warning(self.request, 'You need to be logged in.')
        return redirect('login')



########################### REST API Views ###########################
    

class TaskAPIView(APIView):
    '''Create, Update, Retrive, Delete Task'''
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None): 
        if pk:
            try:
                tasks = Task.objects.get(user = request.user, pk = pk)
                serializer = TaskSerializer(instance=tasks)
                return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
            except Task.DoesNotExist:
                return Response({'status': 'error', 'data': 'Task do not exist'}, status=status.HTTP_400_BAD_REQUEST)
        
        tasks = Task.objects.filter(user = request.user)
        serializer = TaskSerializer(instance=tasks, many = True)
        return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            instance.user = request.user
            instance.save()
            
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'status': 'error', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try: 
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({'status': 'error', 'data': 'Task does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TaskSerializer(task, data=request.data, partial = True)
        if serializer.is_valid():
            instance = serializer.save()
            
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'status': 'error', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try: 
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({'status': 'error', 'data': 'Task does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'status': 'error', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            task = Task.objects.get(user = request.user, pk = pk).delete()
            return Response({'status': 'success', 'data': 'Task Deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            return Response({'status': 'error', 'data': 'task does not exist'}, status=status.HTTP_204_NO_CONTENT)
            
