from django.urls import path, include

from . import views

urlpatterns = [
    path('getCategoryData/<int:cat_id>/', views.getCategoryData ),
    path('getAllCategorySummary/<int:project_id>/', views.getAllCategorySummary ),
    path('getAllCategoryWithTaskName/<int:project_id>/', views.getAllCategoryWithTaskName ),
    path('setDecomposition/', views.setDecomposition ),
    path('editCategories/', views.editCategories ),
    path('updateFuncCat/<int:pk>/', views.UpdateFuncCategory.as_view() ), #use patch here
    path('getCostMonthGraph/', views.getCostMonthGraph ),
    path('updateUserTaskMap/', views.updateUserTaskMap ),
    path('calculateCostAdvanced/', views.calculateCostAdvanced ),
    path('calculateCost/', views.calculateCost ),

]
