
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
        fields = ("name", "due_date", "details",)
        widgets = {
            "due_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                    "placeholder": "Recieved Date",
                    "required": False,
                }
            ), 
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "type": "text",
                    "placeholder": "Note",
                    
                }
            ), 
          
            "details": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "type": "textarea",
                    "placeholder": "Details",
                    
                }
            ), 
            }
    

    # def save(self, commit: bool = True) -> Task:
    #     task: Task = super().save(commit)
    #     task.save()
    #     return task