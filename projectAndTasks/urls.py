from django.urls import path, include

from . import views

urlpatterns = [
    path('addproject/', views.ProjectHandler.as_view()),
    path('getproject/<int:project_id>/', views.ProjectHandler.as_view()),
    path('addtask/', views.TaskHandler.as_view() ),
    path('updateTask/<int:pk>/', views.UpdateTask.as_view() ), #use patch here
    path('updateProject/<int:pk>/', views.UpdateProject.as_view() ), #use patch here
    path('getcomments/', views.getCommentOnTask ),
    path('addcomments/', views.TaskCommentHandler.as_view() ),
    path('addtaskparent/', views.TaskHierarchyHandler.as_view() ),
    path('deleteTask/<int:task_id>/', views.deleteTask ),
    path('deleteProject/<int:pk>/', views.DeleteProject.as_view() ), # use DELETE method
    path('addNotification/', views.NotificationHandler.as_view() ),
    path('getNotification/<int:receiver_id>/', views.NotificationHandler.as_view()),
    path('getUserProjects/<int:user_id>/', views.getUserProjects ),
    path('getAllTasksCatalogue/', views.getAllTasksCatalogue),
    path('getAllTasksCatalogueUser/<int:user_id>/', views.getAllTasksCatalogueUser),
    path('getAllProjectTaskCount/', views.getAllProjectTaskCount ),
    path('getAllProjectTaskCountUser/<int:user_id>/', views.getAllProjectTaskCountUser ),
    path('setAttachments/', views.addStoredFiles ),
    # path('getProjectTreeStructure/<int:project_id>/', views.getProjectTreeStructure ), 
    
]

