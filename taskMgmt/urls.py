from django.urls import path, include

from . import views

urlpatterns = [
    path('getproject_tasks/', views.getAllTasksForProject),
    path('gettaskslist/', views.getOnlyTasksForProject ), # title, priority, due date, status
    path('getsubtasks/', views.getSubTasks ),
    path('gettaskdetails/', views.getTaskDetails ),
]
