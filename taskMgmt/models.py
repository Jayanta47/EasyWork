from django.db import models
from projectAndTasks.models import Task
from userMgmt.models import User

# Create your models here.

class Dependency (models.Model):
    id = models.AutoField(
        primary_key=True
    )

    dependent_on_task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="depending_task"
    )

    parent_task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="parent_of_dependent_task"
    )

class User_Task_Map (models.Model):
    id = models.AutoField(
        primary_key=True
    )

    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    task_id = models.ForeignKey(
        Task,
        on_delete=models.CASCADE
    )

    assign_date = models.DateField(
        auto_now_add=True, null=True
    )

    duration = models.IntegerField(
        default=None,
        null=True
    )

    weekly_effort = models.IntegerField(
        default=0,
        null=True
    )

    wage = models.IntegerField(
        default = 0,
        null = True
    )


class Milestones(models.Model):
    STATUS_LIST = [
        ("Upcoming", "upcoming"),
        ("Ongoing", "ongoing"),
        ("Passed", "passed"),
    ]
    
    id = models.AutoField(
        primary_key=True
    )

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=255,
        default="milestone title"
    )

    description = models.CharField(
        max_length=255,
        default="milestone description"
    )

    status = models.CharField(
        max_length=255,
        choices=STATUS_LIST,
        default="Upcoming"
    )

    creation_date = models.DateField(
        auto_now_add=True,
    )
