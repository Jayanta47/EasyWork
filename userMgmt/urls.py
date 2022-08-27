from django.urls import path, include

from . import views

urlpatterns = [
    path('getallusers/', views.getAllUsersInfo ),
    path('getDesignation/', views.getAllDesignation ),
    path('getUsersUnderDesignation/', views.getUsersUnderDesignation ),
    path('addUser/', views.addUser ),
    path('modifyUser/', views.modifyUser),
    path('getSelectedUsers/', views.getSelectedUsers ),
    path('getUserInfo/<int:user_id>/', views.getUserInfo ),
    path('get_Designation/<int:id>/', views.getDesignation ),
]