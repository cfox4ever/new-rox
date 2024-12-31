




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
    return render (request,"partials/task.html",{"tasks":tasks,"form":form})


