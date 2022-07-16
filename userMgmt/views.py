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