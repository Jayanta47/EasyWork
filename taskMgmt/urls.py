from django.urls import path, include

from . import views

urlpatterns = [
    path('getproject_tasks/', views.getAllTasksForProject),
]
