from django.urls import path, include

from . import views

urlpatterns = [
    path('getCategoryData/<int:cat_id>/', views.getCategoryData ),
    path('getAllCategorySummary/', views.getAllCategorySummary ),
]