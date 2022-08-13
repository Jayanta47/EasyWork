from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import *

@api_view(["GET"])
def getAllUsersInfo(request):
    user_info = User.objects.all().values()

    return Response({"success": True, "user_info":user_info}, status=status.HTTP_200_OK)

@api_view(["GET"])
def getAllDesignation(request):
    all_designation = Designation.objects.all().values("job_name")

    return Response({"success": True, "designation":all_designation}, status=status.HTTP_200_OK) 


@api_view(["POST"])
def getUsersUnderDesignation(request):
    job_name = request.data["job_name"]
    all_members = User.objects.filter(job__job_name=job_name).values("id", "first_name", "last_name", "email")

    return Response({"success": True, "members":all_members}, status=status.HTTP_200_OK) 
