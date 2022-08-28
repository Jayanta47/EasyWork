from django.db import models
# from projectAndTasks.models import Task, Project
from userMgmt.models import User
# Create your models here.


class FuncCategory (models.Model):
    id = models.AutoField(
        primary_key=True
    )

    title = models.CharField(
        max_length=200,
        null=True
    )

    expected_time = models.IntegerField(
        null=True,
        default=0,
    )

    man_hour_per_week = models.IntegerField(
        null=True,
        default=0,
    )

    allocated_budget = models.IntegerField(  # in thousands
        null=True,
        default=0
    )

    loc = models.IntegerField(  # in KLOC unit
        null=True,
        default=0
    )

    loc_per_pm = models.FloatField(
        null=True,
        default=0.0
    )

    cost_per_loc = models.IntegerField(
        null=True,
        default=0
    )

    difficulty = models.CharField(
        max_length=15,
        choices=[
            ("E", "easy"),
            ("M", "medium"),
            ("H", "hard")
        ],
        default="E"
    )

    estimated_cost = models.IntegerField( 
        null=True,
        default=0
    )

    misc_cost = models.IntegerField( 
        null=True,
        default=0
    ) 

# class Category_employee_effort_map (models.Model):
#     id = models.AutoField(
#         primary_key=True
#     )

#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE
#     )
