from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from projectAndTasks.serializers import ProjectSerializer, TaskCommentSerializer, TaskHierarchySerializer, TaskSerializer
from projectAndTasks.serializers import User_Project_Map_Serializer
from .models import Project, Task, TaskComments, TaskHierarchy, User_Project_Map

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
    comments = TaskComments.objects.filter(task=task_id).values()

    for comment in comments:
        comments_list.append(comment)

    return Response({"success": True, "comments_list": comments_list},
                    status=status.HTTP_200_OK)


@api_view(["GET"])
def deleteTask(request, task_id):
    try:
        Task.objects.filter(id=task_id).delete()
        return Response({"success": True}, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST) 

@api_view(["POST"])
def updateTask(request):
    data = request.data
    