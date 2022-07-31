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

    # project_id = models.ForeignKey(
    #     Project,
    #     on_delete=models.CASCADE,
    #     null=False
    # )

    expected_time = models.IntegerField(
        null = True,
        default=0,
    )

    man_hour_per_week = models.IntegerField(
        null = True,
        default=0,
    )

    allocated_budget = models.IntegerField( # in thousands
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



