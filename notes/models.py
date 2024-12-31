from django.db import models
from django.utils.timezone import now
from django.db.models.query import QuerySet
from django.contrib.auth.models import User

from datetime import datetime, timedelta
from django.utils.timezone import now


today = now().date()
next_week_start = today + timedelta(days=(7 - today.weekday()))  # Start of next week
next_week_end = next_week_start + timedelta(days=6)  # End of next week
first_day_of_month = today.replace(day=1)
last_day_of_month = (first_day_of_month + timedelta(days=31)).replace(day=1) - timedelta(days=1)
first_day_of_year = today.replace(month=1, day=1)
last_day_of_year = today.replace(month=12, day=31)
class TaskList(models.Model):
    name = models.CharField( max_length=255)
    user=  models.ForeignKey(
       User,
       on_delete=models.SET_NULL,
       null=True,
       blank=True,
       
   ) 

    

    class Meta:
        verbose_name = "Task List"
        verbose_name_plural = "Task Lists"

    def __str__(self) -> str:
        return self.name

   

    @property
    def is_complete(self) -> bool:
        return not self.tasks.filter(is_done=False).exists()

    @property
    def complete_tasks(self) -> models.QuerySet["Task"]:
        return self.tasks.filter(is_done=True)

    @property
    def incomplete_tasks(self) -> models.QuerySet["Task"]:
        return self.tasks.filter(is_done=False)
    @property
    def notes_due_next_week(self) -> models.QuerySet["Task"]:
        return self.tasks.filter(due_date__date__gte=next_week_start,
                                due_date__date__lte=next_week_end,
                                is_done=False) 
    @property
    def notes_due_this_month(self) -> models.QuerySet["Task"]:
        return self.tasks.filter(due_date__date__gte=first_day_of_month,
                                due_date__date__lte=last_day_of_month,
                                is_done=False
                                )    
    @property
    def notes_due_this_year(self) -> models.QuerySet["Task"]:
        return self.tasks.filter(due_date__date__gte=first_day_of_year,
                                due_date__date__lte=last_day_of_year,
                                is_done=False
                                )
class Task(models.Model):
   user=  models.ForeignKey(
       User,
       on_delete=models.SET_NULL,
       null=True,
       blank=True,
       
   ) 
   task_list = models.ForeignKey(
        TaskList,
        related_name="tasks",
        on_delete=models.CASCADE,
    )
   name = models.CharField(max_length=255)  # Title of the note
   details = models.TextField()  # Detailed content of the note
   due_date = models.DateTimeField()  # Deadline for the note
   is_done = models.BooleanField(default=False)  # Completion status
   completed_at =models.DateTimeField(blank=True,null=True)  # Note creation timestamp
   created_at = models.DateTimeField(auto_now_add=True)  # Note creation timestamp
   updated_at = models.DateTimeField(auto_now=True)  # Note last updated timestamp
   def is_past_due(self):
       """Check if the note is past due and not completed."""
       return not self.is_done and self.due_date < now()
   def __str__(self):
       return self.name