from django.contrib import admin

from .models import Dependency, User_Task, Milestones

# Register your models here.
admin.site.register(Dependency)
admin.site.register(User_Task)
admin.site.register(Milestones)