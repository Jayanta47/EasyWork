from django.db import models
from ..projectAndTasks.models import Task

# Create your models here.

class Dependency (models.Model):
    id = models.AutoField(
        primary_key=True 
    )  

    dependent_on_task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE
    )

    parent_task = models.ForeignKey(
        Task, 
        on_delete=models.CASCADE
    )