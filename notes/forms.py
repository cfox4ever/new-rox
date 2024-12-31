
from django import forms
from django.utils.text import slugify

from .models import Task, TaskList

class TaskListCreateForm(forms.ModelForm):
    

    class Meta:
        model = TaskList
        fields = ("name",)
        
        

        

class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ("name", "is_done","details","due_date")
        widgets = {
            "due_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                    "placeholder": "Recieved Date",
                }
            ), 
            }
    

    def save(self, commit: bool = True) -> Task:
        task: Task = super().save(commit)
        task.save()
        return task