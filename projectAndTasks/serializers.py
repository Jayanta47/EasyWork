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

    # def update(self, instance, validated_data):
    #     # print("project_id", instance.project_id.id)
    #     instance.project_id = validated_data.get('project_id', instance.project_id.id)
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.description = validated_data.get('description', instance.description)
    #     instance.creation_time = validated_data.get('creation_time', instance.creation_time)
    #     instance.start_time = validated_data.get('start_time', instance.start_time)
    #     instance.end_time = validated_data.get('end_time', instance.end_time)
    #     instance.slack_time = validated_data.get('slack_time', instance.slack_time)
    #     instance.status = validated_data.get('status', instance.status)
    #     instance.category_id = validated_data.get('category_id', instance.category_id)
    #     instance.save()
    #     return instance

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
    # comment_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = TaskComments
        fields = '__all__'