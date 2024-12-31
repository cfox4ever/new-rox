from django.urls import path

from .views import (tasks,task_list_delete,task)

urlpatterns = [
    
    
    path("tasks/", tasks, name="tasks"),
    path("task_list_delete/<int:pk>/", task_list_delete, name="task_list_delete"),
    path("task/<int:pk>/", task, name="task"),
    
]