import imp
from django.contrib import admin

from .models import Project, Task, User_Project_Map, TaskHierarchy

# Register your models here.

admin.site.register(Project)
admin.site.register(Task)
admin.site.register(User_Project_Map)
admin.site.register(TaskHierarchy)
