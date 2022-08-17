import imp
from rest_framework import serializers

from .models import User

class UserSerializer(serializers.ModelSerializer):
    # full_name = serializers.Field()


    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            'password',
            "email",
            "mobile",
            "address",
            "date_of_birth",
            "gender",
            "job",
            "joining_date",
        ]
        extra_kwargs = {
            'password': {'write_only':True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
