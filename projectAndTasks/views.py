from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import generics

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
        comments_list.append(comment.data)

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