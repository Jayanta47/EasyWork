from django.urls import path, include

from . import views

urlpatterns = [
    path('getproject_tasks/', views.getAllTasksForProject),
    path('getprojects/', views.getProjects ),
    path('gettaskslist/', views.getOnlyTasksForProject ), # title, priority, due date, status
    path('getsubtasks/', views.getSubTasks ),
    path('gettaskdetails/', views.getTaskDetails ),
    path('getTest/<int:param1>/<int:param2>/', views.getTest ),
    path('getDepenency/<int:dependency_id>/', views.DependencyHandler.as_view() ),
    path('addDependency/', views.DependencyHandler.as_view() ),
    path('deleteDependency/<int:dependency_id>/', views.deleteDependency ),
    path('assignUser/', views.assignUser ),
    path('getDependencyGraph/', views.getDependencyGraph ),
    path('getTaskPriority/', views.getTaskPriority),
    path('addMilestone/', views.MilestoneHandler.as_view() ),
    path('deleteMilestone/', views.DeleteMilestone.as_view() ), # use DELETE here
    path('updateMilestone/<int:pk>', views.UpdateMilestone.as_view() ), # use patch here
    path('getMilestone/<int:milestone_id>/', views.MilestoneHandler.as_view()),
]
