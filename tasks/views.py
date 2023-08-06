from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from tasks.forms import TaskForm
from tasks.models import Task


# Create your views here.
def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':
        print('enviando interfaz formulario')
        print(request.GET)
        return render(request, 'singup.html', {
            'form': UserCreationForm
        })
    elif request.method == 'POST':
        print("---Obteniedo datos del cliente---")
        print(request.POST)
        print(request.GET)
        print("-----------------------")

        if request.POST['password1'] == request.POST['password2']:
            try:
                user: User = User.objects.create_user(request.POST['username'], None, request.POST['password1'])
                user.save()

                login(request, user)
                return redirect('tasks')
            except IntegrityError as err:
                print("IntegrityError:", err)
                return render(request, 'singup.html', {
                    'form': UserCreationForm,
                    'error': 'El usuario ya existe'
                })
            except Exception as err:
                return HttpResponse(f"<h1>Error:{err}</h1>")
        return render(request, 'singup.html', {
            'form': UserCreationForm,
            'error': 'Contraseña no coincide'
        })


@login_required
def tasks(request):
    tareas = Task.objects.filter(user=request.user, datecomplete__isnull=True)

    return render(request, 'tasks.html', {
        'tasks': tareas  # todas las tareas que estan en
        # la base da datos
    })


@login_required
def tasks_complete(request):
    tareas = Task.objects.filter(user=request.user, datecomplete__isnull=False).order_by('datecomplete')

    return render(request, 'tasks.html', {
        'tasks': tareas  # todas las tareas que estan en
        # la base da datos
    })


@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        # el metodo es post
        try:
            form = TaskForm(request.POST)
            new_tasks: Task = form.save(commit=False)
            new_tasks.user = request.user
            new_tasks.save()
            return redirect('tasks')
        except Exception as err:
            print("Exepcion: ", err, "tipo:", type(err), "arg:", err.args)
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'err': 'Porfavor provee datos validos'
            })


@login_required
def task_detail(request, task_id: int):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {
            'task': task,
            'form': form
        })
    else:
        try:
            print(request.POST)
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
                'task': task,
                'form': form,
                'error': "error actualizando tarea"
            })


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecomplete = timezone.now()
        task.save()
        return redirect('tasks')


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')



@login_required
def signout(request):
    logout(request)
    return redirect('home')


def sigin(request):
    if request.method == 'GET':
        return render(request, 'sigin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        print("tipo valor user:", user)

        if user is None:
            return render(request, 'sigin.html', {
                'form': AuthenticationForm,
                'err': 'Usuario o contraseña incorrecto'
            })
        else:
            print("usuario si existe, redirigiendo")
            login(request, user)
            return redirect('tasks')
