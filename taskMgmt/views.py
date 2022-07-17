from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from projectAndTasks.models import Project


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

    return Response({"task_list": task_list, "dependency_list": dependency_list},
                    status=status.HTTP_200_OK)


@api_view(["POST"])
def getSubTasks(request):
    task_id = request.data['task_id']
    subtask_list = getSubTaskList(task_id)
    return Response({"subtask_list": subtask_list, "success": True}, status=status.HTTP_200_OK)


@api_view(["POST"])
def getTaskDetails(request):
    task_id = request.data['task_id']
    print(task_id)
    task_info = getTaskDetailsDict(task_id)
    return Response({"success": True, "task_info": task_info}, status=status.HTTP_200_OK)


@api_view(["POST"])
def getOnlyTasksForProject(request):
    project_id = request.data['project_id']
    task_list = getTasksList(project_id=project_id)
    return Response({"task_list": task_list}, status=status.HTTP_200_OK)

@api_view(["POST"])
def getProjects(request):
    project_list = []
    projects = Project.objects.all().values()
    for project in projects:
        project['remaining_time'] = getRemainingTime(project['start_date'], project['allocated_time'])
        project_list.append(project)
    return Response({"project_list": project_list, "success": True}, status=status.HTTP_200_OK)