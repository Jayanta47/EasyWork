from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


from .utils import *


@api_view(["POST"])
def getAllTasksForProject(request):
    project_id = request.data['project_id']
    task_list = getTasksList(project_id=project_id)
    task_id_list = []
    for task in task_list:
        task_id = task['id']
        task_id_list.append(task_id)
    dependency_list = getPredecessorTaskList(task_id_list=task_id_list)

    return Response({"task_list": task_list, "dependency_list": dependency_list}, status=status.HTTP_200_OK)
