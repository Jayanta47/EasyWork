from rest_framework import serializers

from taskMgmt.models import Dependency, Milestones, User_Task


class DependencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dependency
        fields = [
            'id',
            'dependent_on_task',
            'parent_task',
        ]


class MilestonesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milestones
        fields = [
            'id',
        ]


class User_TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Task
        fields = [
            'id',
            'user_id',
            'task_id',
            'assign_date',
            'duration',
        ]
