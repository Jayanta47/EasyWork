from django.urls import path, include

from . import views

urlpatterns = [
    path('getallusers/', views.getAllUsersInfo ),
    path('getDesignation/', views.getAllDesignation ),
    path('getUsersUnderDesignation/', views.getUsersUnderDesignation ),
]