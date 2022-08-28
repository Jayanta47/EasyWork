from pyexpat import model
from django.db import models
from userMgmt.models import Designation, User
from costEstimation.models import FuncCategory
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
        default=None, null=True
    )  # in number of days

    budget = models.IntegerField(
        default=1000,
        null=True
    )

    dev_type = models.CharField(
        max_length=100,
        default=None,
        null=True
    )


class User_Project_Map(models.Model):
    id = models.AutoField(
        primary_key=True
    )

    user_id = models.ForeignKey(
        User,
        null=False,
        on_delete=models.CASCADE
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
        auto_now_add=True
    )

    duration = models.IntegerField(
        null=False,
        default=None,
    )


class Task(models.Model):

    STATUS_LIST = [
        ("Completed", "completed"),
        ("Ongoing", "ongoing"),
        ("Postponed", "postponed"),
        ("Not Started", "not started"),
    ]

    id = models.AutoField(
        primary_key=True
    )

    project_id = models.ForeignKey(
        Project,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=200,
        default="title",
        null=True,
    )

    description = models.CharField(
        max_length=600,
        default=None,
        null=True
    )

    creation_time = models.DateTimeField(
        auto_now_add=True
    )

    start_time = models.DateField(
        default=None,
        null=True,
    )

    end_time = models.DateField(
        default=None,
        null=True
    )

    slack_time = models.IntegerField(
        default=0,
        null=True
    )

    status = models.CharField(
        max_length=15,
        choices=STATUS_LIST,
        default="Not Started"
    )

    category_id = models.ForeignKey(
        FuncCategory,
        on_delete=models.SET_NULL,
        default=None,
        null=True
    )


class TaskHierarchy (models.Model):
    id = models.AutoField(
        primary_key=True
    )

    parent_task_id = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="parent_task"
    )

    sub_task_id = models.ForeignKey(
        Task,
        null=False,
        on_delete=models.CASCADE,
        related_name="sub_task"
    )


class TaskComments (models.Model):
    id = models.AutoField(
        primary_key=True
    )

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        default=None,
        on_delete=models.CASCADE
    )

    comment = models.CharField(
        max_length=1000,
        null=False,
    )

    comment_time = models.DateTimeField(
        auto_now_add=True,
    )


class Project_Category_Map (models.Model):
    id = models.AutoField(
        primary_key=True
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE
    )

    category = models.ForeignKey(
        FuncCategory,
        on_delete=models.CASCADE
    )


class Notification (models.Model):
    id = models.AutoField(
        primary_key=True
    )

    task = models.ForeignKey(
        Task, 
        on_delete=models.CASCADE,
        null=True
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sender"
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="receiver"
    )

    text = models.CharField(
        max_length=255
    )

    notification_time = models.DateTimeField(
        auto_now_add=True 
    )


class StoredFiles(models.Model):
    id = models.AutoField(
        primary_key=True
    )

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE
    )

    file_url = models.URLField(
        max_length=500
    )

