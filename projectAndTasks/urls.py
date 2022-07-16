from django.urls import path, include

from . import views

urlpatterns = [
    path('addproject/', views.ProjectHandler.as_view()),
    path('getproject/<int:project_id>/', views.ProjectHandler.as_view()),
]