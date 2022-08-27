import imp
from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from projectAndTasks.models import Project, Task, User_Project_Map
from taskMgmt.ml_util import getPriorityOfTask
from taskMgmt.serializers import DependencySerializer, MilestonesSerializer, User_TaskSerializer

from .utils import *
from .models import Dependency, Milestones, User_Task_Map

from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

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
    proj_title = Project.objects.filter(id=project_id).values()
    if len(proj_title) > 0:
        proj_title = proj_title[0]["title"]
    else:
        proj_title = "Not found"
    print(proj_title)
    task_list = getTasksList(project_id=project_id)
    return Response({"task_list": task_list, "title": proj_title}, status=status.HTTP_200_OK)


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


@api_view(["POST"])
def assignUser(request):
    project_id = request.data['project_id']
    task_id = request.data['task_id']
    abc = User.objects.all().values()
    print(abc)
    print(request.data)
    if task_id != -1:
        for member_id in request.data["members"]:
            task = Task.objects.filter(id=task_id).values("start_time", "end_time")[0]
            # print("time", task["end_time"])
            duration = task["end_time"] - task["start_time"] 
            duration = duration.days
            # duration = datetime.datetime(2015,11,15)
            user = User.objects.get(id = member_id)
            task = Task.objects.get(id=task_id)
            i = User_Task_Map(user_id = user, task_id=task, duration=duration)
            i.save()
    
    for member_id in request.data["members"]:
        project = Project.objects.filter(id=project_id).values("allocated_time")[0]
        duration = project["allocated_time"]
        user = User.objects.get(id=member_id)
        role = Designation.objects.get(id=user.job_id)
        project = Project.objects.get(id = project_id)
        i = User_Project_Map(user_id = user, project_id=project, duration=duration, project_role=role)
        i.save()
    return Response({"success": True}, status=status.HTTP_200_OK)


@api_view(["POST"])
def getDependencyGraph(request):
    project_id = request.data['project_id']
    task_id = request.data['task_id']

    title = 'title'

    if task_id == -1:
        task_list = getTasksList(project_id=project_id)
        project = Project.objects.filter(id=project_id).values()[0]
        title = project["title"]
    else:
        task_list = getSubTaskList(task_id)
        task = Task.objects.filter(id=task_id).values()[0]
        title = task["title"]

    if len(task_list) == 0:
        return Response({"success": True, "data": []}, status=status.HTTP_200_OK)
    ancestor_list = []
    predecessor_list = []
    duration_list = []
    task_id_list = [task['id'] for task in task_list]
    map, task_id_list, ancestor_list, predecessor_list, duration_list = getPredGraphList(task_id_list)
    # print(task_id_list, ancestor_list, predecessor_list, duration_list)

    ancestry = {
        "ac": ancestor_list,
        "pr": predecessor_list,
        "du": duration_list
    }
    img_name = generateDependencyGraph(ancestry)
    maplist = []
    for key, value in map.items():
        maplist.append(value)
    data = {
        "task_map": maplist,
        "image_name": img_name,
        "title": title
    }

    return Response({"success": True, "data": data}, status=status.HTTP_200_OK)

@api_view(["POST"])
def getTaskPriority(request):
    project_id = request.data['project_id']
    task_id = request.data['task_id']
    user_id = request.data['user_id']

    if task_id == -1:
        task_list = getUserTaskList(project_id, user_id)
    else:
        task_list = getUserSubTaskList(task_id, user_id)

    if len(task_list) == 0:
        return Response({"success": True, "data": []}, status=status.HTTP_200_OK)

    priority_list = []
    for task in task_list:
        label, point = getPriorityOfTask(task['id'])
        d = {
            "task_id": task['id'],
            "priority": label,
            "priority_point": point,
            "title": task["title"],
            "end_time": task["end_time"],
        }
        priority_list.append(d)

    priority_list = sorted(priority_list, key=lambda x: x["priority_point"], reverse=True)
    
    

    return Response({"priority_list": priority_list}, status=status.HTTP_200_OK)