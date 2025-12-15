from django.shortcuts import render
from django.http import Http404
from .models import Todo

def todo_list(request):
    todos = Todo.objects.all()
    return render(request, 'todo/todo_list.html', {'data': todos})

def todo_info(request, todo_id):
    try:
        todo = Todo.objects.get(id=todo_id)
        return render(request, 'todo/todo_info.html', {'data': todo})
    except Todo.DoesNotExist:
        raise Http404("Todo not found")
