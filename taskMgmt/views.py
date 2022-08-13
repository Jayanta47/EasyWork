import imp
from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from projectAndTasks.models import Project
from taskMgmt.serializers import DependencySerializer, MilestonesSerializer, User_TaskSerializer

from .utils import *
from .models import Dependency, Milestones, User_Task

from django.core.exceptions import ObjectDoesNotExist

class DependencyHandler (
    APIView
):
    def post(self, request):
        serializer = DependencySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, dependency_id, *args, **kwargs):
        project_data = Dependency.objects.filter(id=dependency_id).values()
        print(project_data)
        serializer = DependencyHandler(data=project_data, may=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# class MilestoneHandler (APIView):
#     def post(self, request):
#         serializer = MilestonesSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def get(self, request, project_id, *args, **kwargs):
#         project_data = Project.objects.filter(id=project_id).values()
#         # for p in project_data:
#         #     print(p)
#         print(project_data)
#         serializer = ProjectHandler(data=project_data, may=True)

#         return Response(serializer.data, status=status.HTTP_200_OK)


class User_TaskHandler (
    APIView
):
    def post(self, request):
        serializer = User_TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, project_id, *args, **kwargs):
        project_data = User_TaskHandler.objects.filter(id=project_id).values()
        # for p in project_data:
        #     print(p)
        print(project_data)
        serializer = User_TaskHandler(data=project_data, may=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


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
        project['remaining_time'] = getRemainingTime(
            project['start_date'], project['allocated_time'])
        project_list.append(project)
    return Response({"project_list": project_list, "success": True}, status=status.HTTP_200_OK)


@api_view(["GET"])
def getTest(request, param1, param2):
    print(param1, param2)
    return Response({"success": True}, status=status.HTTP_200_OK)

@api_view(["GET"])
def deleteDependency(request, dependency_id):
    try:
        Dependency.objects.filter(id=dependency_id).delete()
        return Response({"success": True}, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST) 