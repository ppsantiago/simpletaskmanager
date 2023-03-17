from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import CreateTaskForm
from .models import Task

# Create your views here.

def home(request):
    return render(request, 'home.html', {
    })


def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # Register User
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {'form': UserCreationForm, 'message': 'User already exists'})
        else:
            return render(request, 'signup.html', {'form': UserCreationForm, 'message': 'Password do not match'})
       
        
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html',{
            'form': AuthenticationForm,
            'form2': UserCreationForm,
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            print('errr')    
            return render(request, 'signin.html',{
                'form': AuthenticationForm, 
                'message' : 'Usuario o password invalido',
                'form2': UserCreationForm,

            })
        else:
            login(request, user)
            return redirect('tasks')


@login_required
def task(request):
    tasks = Task.objects.filter(user=request.user)
    # tasks = get_object_or_404.(task)
    return render(request, 'task.html', {'tasks' : tasks})


@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {'form' : CreateTaskForm})
    else:
        try:
            form = CreateTaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            form.save()
            # return render(request, 'create_task.html', {'form' : CreateTaskForm})
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {'form' : CreateTaskForm, 'message' : 'Ingresa datos correctos'})


@login_required
def task_detail(request, task_id):
    
    if request.method == 'GET':    
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = CreateTaskForm(instance=task)
        print(task)
        return render(request, 'taskdetail.html', {'task':task, 'form' : form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = CreateTaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
             return render(request, 'taskdetail.html', {'task':task, 'form' : form, 'message' : 'Error updating task'})


@login_required
def task_complete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')


@login_required    
def task_incomplete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = None
        task.save()
        return redirect('tasks')


@login_required    
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
    
    