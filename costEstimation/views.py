from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import FuncCategory
from taskMgmt.utils import getAllTasksOfCategory


@api_view(["GET"])
def getCategoryData(request, cat_id):
    print(cat_id)
    category = FuncCategory.objects.filter(id=cat_id).values()[0]
    # print(category)
    all_tasks = getAllTasksOfCategory(cat_id=cat_id)
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
        print(category)
        all_tasks = getAllTasksOfCategory(cat_id=category['id'])
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
