from django.contrib import admin

from .models import Dependency, User_Task_Map, Milestones

# Register your models here.
admin.site.register(Dependency)
admin.site.register(User_Task_Map)
admin.site.register(Milestones)