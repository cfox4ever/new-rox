




from django.shortcuts import get_object_or_404, render


from .filters import TaskListFilter
from .forms import TaskForm, TaskListCreateForm
from .models import Task, TaskList



def tasks(request):
    form = TaskListCreateForm()
    lists = TaskList.objects.filter(user=request.user)
   
    if request.method == 'POST' :
        
        form = TaskListCreateForm(request.POST or None )
        if form.is_valid():
            task_list = form.save(commit=False)
            task_list.user = request.user
            task_list.save()
            form = TaskListCreateForm()
    if request.htmx:
        
        lists = TaskList.objects.filter(user=request.user)
        return render (request,"partials/task_list.html",{"lists":lists})
    cont = {"form":form,"lists":lists}
    return render(request,'tasks.html',cont)

def task_list_delete(request,pk):
    list = TaskList.objects.filter(id=pk)
    list.delete()
    lists = TaskList.objects.filter(user=request.user)
    return render (request,"partials/task_list.html",{"lists":lists})

    
def task(request,pk):
    list = TaskList.objects.get(id=pk)
    tasks = Task.objects.filter(task_list=list)
    
    form = TaskForm()
    if request.method == "POST":
        form = TaskForm(request.POST or None)
        if form.is_valid():
            task_item = form.save(commit=False)
            task_item.task_list = list
            task_item.save()
            form = TaskForm()
            tasks = Task.objects.filter(task_list=list)
            return render (request,"partials/tasks.html",{"tasks":tasks})
        
    return render (request,"partials/task.html",{"tasks":tasks,"task_list":list,"form":form})


def task_completed(request,pk):
    task = Task.objects.get(id=pk)
    task.is_done = not task.is_done
    task.save()
    list = task.task_list
    tasks = Task.objects.filter(task_list=list)
    return render (request,"partials/tasks.html",{"tasks":tasks})