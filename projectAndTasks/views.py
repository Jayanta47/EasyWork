from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from projectAndTasks.serializers import ProjectSerializer, TaskHierarchySerializer, TaskSerializer

from .models import Project, Task, TaskHierarchy, User_Project_Map


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
        serializer = User_Project_Map(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, project_id, *args, **kwargs):
        project_data = Task.objects.filter(id=project_id).values()
        serializer = TaskSerializer(data=project_data, may=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskHierarchyHandler(APIView):
    def post(self, request):
        serializer = TaskHierarchy(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, project_id, *args, **kwargs):
        project_data = TaskHierarchy.objects.filter(id=project_id).values()
        serializer = TaskHierarchySerializer(data=project_data, may=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
