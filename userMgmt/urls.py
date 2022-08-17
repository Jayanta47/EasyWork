from django.urls import path, include

from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view()), 
    path('getallusers/', views.getAllUsersInfo ),
    path('getDesignation/', views.getAllDesignation ),
    path('getUsersUnderDesignation/', views.getUsersUnderDesignation ),
    path('addUser/', views.addUser ),
    path('registerUser/', views.RegisterView.as_view()),
    path('updateUser/<int:pk>/', views.UpdateUser.as_view()),
    path('getSelectedUsers/', views.getSelectedUsers )
]