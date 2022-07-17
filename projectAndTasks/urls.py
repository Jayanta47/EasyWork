from django.urls import path, include

from . import views

urlpatterns = [
    path('addproject/', views.ProjectHandler.as_view()),
    path('getproject/<int:project_id>/', views.ProjectHandler.as_view()),
    path('addtask/', views.TaskHandler.as_view() ),
    path('getcomments/', views.getCommentOnTask ),
    path('addcomments/', views.TaskCommentHandler.as_view() ),
    path('addtaskparent/', views.TaskHierarchyHandler.as_view() ),
]