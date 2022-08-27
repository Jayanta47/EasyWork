import imp
from rest_framework import serializers

from .models import Designation, User

class UserSerializer(serializers.ModelSerializer):
    # full_name = serializers.Field()


    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "mobile",
            "address",
            "date_of_birth",
            "gender",
            "job",
            "joining_date",
        ]

class DesignationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Designation
        fields = ["__all__"]