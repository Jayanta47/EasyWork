import imp
from django.contrib import admin

from .models import Notification, Project, Task, TaskComments, User_Project_Map, TaskHierarchy, Project_Category_Map

# Register your models here.

admin.site.register(Project)
admin.site.register(Task)
admin.site.register(User_Project_Map)
admin.site.register(TaskHierarchy)
admin.site.register(TaskComments)
admin.site.register(Project_Category_Map)
admin.site.register(Notification)