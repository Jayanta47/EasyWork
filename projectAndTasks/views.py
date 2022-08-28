from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import generics

from projectAndTasks.serializers import NotificationSerializer, ProjectSerializer, TaskCommentSerializer, TaskHierarchySerializer, TaskSerializer
from projectAndTasks.serializers import User_Project_Map_Serializer
from taskMgmt import serializers
from .models import Notification, Project, Task, TaskComments, TaskHierarchy, User_Project_Map
from userMgmt.models import User
from django.core.exceptions import ObjectDoesNotExist


class ProjectHandler (
    APIView
):
    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, project_id, *args, **kwargs):
        project_data = Project.objects.filter(id=project_id).values()
        # for p in project_data:
        #     print(p)
        print(project_data)
        serializer = ProjectHandler(data=project_data, may=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskHandler(APIView):
    def post(self, request):
        print(request.data)
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, task_id, *args, **kwargs):
        project_data = Task.objects.filter(id=task_id).values()
        serializer = TaskSerializer(data=project_data, may=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class User_Project_Map_Handler(APIView):
    def post(self, request):
        serializer = User_Project_Map_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def get(self, request, project_id, *args, **kwargs):
    #     project_data = User_Project_Map.objects.filter(id=project_id).values()
    #     serializer = TaskSerializer(data=project_data, may=True)

    #     return Response(serializer.data, status=status.HTTP_200_OK)


class TaskHierarchyHandler(APIView):
    def post(self, request):
        serializer = TaskHierarchySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, project_id, *args, **kwargs):
        project_data = TaskHierarchy.objects.filter(id=project_id).values()
        serializer = TaskHierarchySerializer(data=project_data, may=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskCommentHandler(APIView):
    def post(self, request):
        print(request.data)
        serializer = TaskCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def get(self, request, task_id, *args, **kwargs):
    #     project_data = TaskComments.objects.filter(id=comment_id).values()
    #     serializer = TaskCommentSerializer(data=project_data, may=True)

    #     return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def getCommentOnTask(request):
    task_id = request.data["task_id"]
    comments_list = []
    comments = TaskComments.objects.filter(task=task_id)

    for comment in comments:
        comment = TaskCommentSerializer(comment)
        user_id = comment.data['user']
        user_name = User.objects.filter(id=user_id).values(
            'first_name', 'last_name').first()
        # print(user_name)
        comment.data['user_name'] = user_name
        comments_list.append(
            {"comment": comment.data, "user": user_name["first_name"]+" " + user_name["last_name"]})

    return Response({"success": True, "comments_list": comments_list},
                    status=status.HTTP_200_OK)


@api_view(["GET"])
def deleteTask(request, task_id):
    try:
        Task.objects.filter(id=task_id).delete()
        return Response({"success": True}, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)

# @api_view(["POST"])
# def updateTask(request):
#     data = request.data

#     task_id = data["id"]
#     task = Task.objects.get(id=task_id)
#     # print("project_id", task.project_id.id)
#     # task.project_id = task.project_id.id

#     task_serializer = TaskSerializer(task, data=data)

#     if task_serializer.is_valid():
#         task_serializer.save()
#         return Response(task_serializer.data, status=status.HTTP_200_OK)
#     else:
#         print(task_serializer.data)
#         return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)


class UpdateTask(generics.UpdateAPIView):
    queryset = Task.objects.all()

    serializer_class = TaskSerializer


# @api_view(["GET"])
# def getProjectTreeStructure(request, project_id):
#     all_tasks_in_project = Task.objects.all().values("id")

#     current_level = []
#     depth = 1
#     isEnd = False

#     for task in all_tasks_in_project:
#         if TaskHierarchy.objects.filter(sub_task_id_id = task["id"]).count() == 0:
#             current_level.append(task)


#     return Response({"success": True}, status=status.HTTP_200_OK)

class UpdateProject(generics.UpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class DeleteProject(generics.DestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class NotificationHandler(APIView):
    def post(self, request):
        serializer = NotificationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, receiver_id):
        print(receiver_id)
        all_notifications = Notification.objects.filter(sender__id=receiver_id)
        data = []
        for notification in all_notifications:
            serializer = NotificationSerializer(notification)
            task = Task.objects.filter(
                id=serializer.data['task']).values().first()
            sender = User.objects.get(id=serializer.data["sender"])
            project = Project.objects.filter(id=task["id"]).values().first()
            d = {
                "task_id": serializer.data["task"],
                "task_title": task["title"],
                "user_id": serializer.data["sender"],
                "user_name": sender.first_name + " " + sender.last_name,
                "project_id": project["id"],
                "project_title": project["title"],
                "date_of_notification": serializer.data["notification_time"],
                "notification_text": serializer.data["text"]
            }

            data.append(d)

        return Response({"data": data}, status=status.HTTP_200_OK)


@api_view(["GET"])
def getUserProjects(request, user_id):
    all_project_map = User_Project_Map.objects.filter(user_id=user_id)
    project_list = []
    for project_map in all_project_map:
        project = project_map.project_id

        serializer = ProjectSerializer(project)
        project_list.append(serializer.data)

    return Response({"data": project_list}, status=status.HTTP_200_OK)


# ("Completed", "completed"),
# ("Ongoing", "ongoing"),
# ("Postponed", "postponed"),
# ("Not Started", "not started"),

@api_view(["GET"])
def getAllTasksCatalogue(request):
    all_tasks = Task.objects.all().values()
    catalogue = {
        "Completed": 0,
        "Ongoing": 0,
        "Postponed": 0,
        "Not Started": 0
    }
    for task in all_tasks:
        if (task["status"] == "Completed"):
            catalogue["Completed"] += 1
        elif (task["status"] == "Ongoing"):
            catalogue["Ongoing"] += 1

        elif (task["status"] == "Postponed"):
            catalogue["Postponed"] += 1

        else:
            catalogue["Not Started"] += 1

    return Response({"catalogue": catalogue}, status=status.HTTP_200_OK)



