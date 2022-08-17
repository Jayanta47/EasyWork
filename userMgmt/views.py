import imp
from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.exceptions import AuthenticationFailed

from .serializers import UserSerializer
from projectAndTasks.models import User_Project_Map
from taskMgmt.models import User_Task_Map

from .models import *


@api_view(["GET"])
def getAllUsersInfo(request):
    user_info = User.objects.all().values()

    return Response({"success": True, "user_info": user_info}, status=status.HTTP_200_OK)


@api_view(["GET"])
def getAllDesignation(request):
    all_designation = Designation.objects.all().values("job_name")

    return Response({"success": True, "designation": all_designation}, status=status.HTTP_200_OK)


@api_view(["POST"])
def getUsersUnderDesignation(request):
    job_name = request.data["job_name"]
    all_members = User.objects.filter(job__job_name=job_name).values(
        "id", "first_name", "last_name", "email")

    return Response({"success": True, "members": all_members}, status=status.HTTP_200_OK)


@api_view(["POST"])
def addUser(request):
    data = request.data

    userSerializer = UserSerializer(data=data)
    if userSerializer.is_valid():
        userSerializer.save()
        return Response(userSerializer.data, status=status.HTTP_200_OK)
    else:
        print(userSerializer.data)
        return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)

class UpdateUser(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(["POST"])
def modifyUser(request):
    data = request.data

    user = User.objects.get(id=data["id"])
    userSerializer = UserSerializer(user, data=data)
    if userSerializer.is_valid():
        userSerializer.save()
        return Response(userSerializer.data, status=status.HTTP_200_OK)
    else:
        print(userSerializer.data)
        return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def getSelectedUsers(request):
    data = request.data

    project_id = data["project_id"]
    task_id = data["task_id"]

    if task_id == -1:
        all_users_map = User_Project_Map.objects.filter(project_id_id=project_id).values()
        # print(all_users_map)
    else :
        all_users_map = User_Task_Map.objects.filter(task_id_id=task_id).values()

    all_user_data = []

    for user_map in all_users_map:
        user_data = User.objects.filter(id=user_map['user_id_id']).values()[0]
        job_id = user_data["job_id"]
        job_name = Designation.objects.filter(id=job_id).values("job_name")[0]
        user_data["designation"] = job_name["job_name"]
        all_user_data.append(user_data)

    return Response({"success": True, "members": all_user_data}, status=status.HTTP_200_OK)


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data["password"]

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("User Not Found")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect Password")

        return Response({"success": True})