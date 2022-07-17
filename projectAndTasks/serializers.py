from dataclasses import fields
from rest_framework import serializers

from projectAndTasks.models import Project, TaskComments, User_Project_Map, Task, TaskHierarchy

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id', 
            'title', 
            'description', 
            'start_date', 
            'allocated_time',
            'budget',
            'dev_type'
        ]

class User_Project_Map_Serializer(serializers.ModelSerializer):

    class Meta:
        model = User_Project_Map
        fields = [
            'id', 
            'user_id', 
            'project_id', 
            'project_role', 
            'start_date', 
            'duration'
        ]

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = [
            'id', 
            'project_id', 
            'title', 
            'description',
            'creation_time', 
            'start_time', 
            'end_time', 
            'slack_time', 
            'status', 
            'category_id'
        ]

class TaskHierarchySerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskHierarchy
        fields = [ 
            'id', 
            'parent_task_id', 
            'sub_task_id', 
        ]


class TaskCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskComments
        fields = [ 
            'id', 
            'task',
            'comment'
        ]