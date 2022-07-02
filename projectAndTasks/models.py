from django.db import models
from requests import delete
from ..userMgmt.models import Designation, User
# Create your models here.


class Project(models.Model):

    id = models.AutoField(
        primary_key=True 
    )

    title = models.CharField(
        max_length=200,
        default="Project",
        null=False 
    )

    description = models.CharField(
        max_length=500
    )

    start_date = models.DateField(
        auto_now_add=True
    )

    allocated_time = models.IntegerField(

    ) # in number of days 

    budget = models.IntegerField(

    )

    dev_type = models.CharField(
        
    )


class User_Project_Map(models.Model):
    id = models.AutoField(
        primary_key=True
    )

    user_id = models.ForeignKey(
        User,
        null = False,
        on_delete = models.CASCADE
    )

    project_id = models.ForeignKey(
        Project,
        null=False,
        on_delete=models.CASCADE
    )

    project_role = models.ForeignKey(
        Designation,
        on_delete=models.CASCADE,
        null=False
    )

    start_date = models.DateField(
        default = None,
    )

    duration = models.IntegerField(
        null = False,
        default=None,
    )

