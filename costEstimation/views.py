from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin

from .models import FuncCategory
from taskMgmt.utils import getAllMembersOfCategory, getAllTasksOfCategory, updateTaskFuncCategory

from .serializers import FuncCategorySerializer

@api_view(["GET"])
def getCategoryData(request, cat_id):
    print(cat_id)
    category = FuncCategory.objects.filter(id=cat_id).values()[0]
    # print(category)
    all_tasks = getAllMembersOfCategory(cat_id=cat_id)
    d = {
        "category_name": category['title'],
        "expected_time": category['expected_time'],
        "allocated_budget": category['allocated_budget'],
        "man_hour_per_week": category['man_hour_per_week'],
        "allocated_members": all_tasks,
    }

    # print("all",all_tasks)
    # employee_list = []
    # for task in all_tasks:

    return Response({"success": True, "data": d},
                    status=status.HTTP_200_OK)


@api_view(["GET"])
def getAllCategorySummary(request):
    d = []
    all_categories = FuncCategory.objects.all().values()

    for category in all_categories:
        # print(category)
        all_tasks = getAllMembersOfCategory(cat_id=category['id'])
        people_assigned = 0
        for x in all_tasks:
            people_assigned = people_assigned+1
        d_ = {
            "category_name": category['title'],
            "expected_time": category['expected_time'],
            "allocated_budget": category['allocated_budget'],
            "man_hour_per_week": category['man_hour_per_week'],
            "allocated_members": people_assigned
        }
        d.append(d_.copy())
    return Response({"success": True, "data": d},
                    status=status.HTTP_200_OK)


@api_view(["GET"])
def getAllCategoryWithTaskName(request):
    data = []
    all_categories = FuncCategory.objects.all().values()

    for category in all_categories:
        print(category)
        all_tasks = getAllTasksOfCategory(cat_id=category['id'])
        print("tasks",all_tasks)

        category_data = {
            "id": category["id"],
            "title": category["title"],
            "tasks": all_tasks
        }

        data.append(category_data)
    print(data)

    return Response({"success": True, "data": data},
                    status=status.HTTP_200_OK)

@api_view(["POST"])
def setDecomposition(request):
    data = request.data["data"]

    for category_data in data:
        tasks = category_data["tasks"]
        for task in tasks:
            updateTaskFuncCategory(task["id"], category_data["id"])
        
    deletion_list = request.data["toDelete"]

    for category_id in deletion_list:
        FuncCategory.objects.filter(id = category_id).delete()

    return Response({"success": True}, status=status.HTTP_200_OK)


@api_view(["POST"])
def editCategories(request):
    category_create_list = request.data['toCreate']
    new_category_list = []
    for new_category_title in category_create_list:
        funcSerializer = FuncCategorySerializer(data={"title":new_category_title})
        if funcSerializer.is_valid():
            funcSerializer.save()
            new_category_list.append(funcSerializer.data)
    
    category_modify_list = request.data['toModify']
    
    for category_data in category_modify_list:
        funcData = FuncCategory.objects.get(id = category_data['id'])
        print(funcData)
        funcSerializer = FuncCategorySerializer(funcData, data=category_data)
        if funcSerializer.is_valid():
            funcSerializer.save()
    
    return Response({"success": True}, status=status.HTTP_200_OK)