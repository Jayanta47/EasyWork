from datetime import datetime, timedelta
from projectAndTasks.models import Task, TaskHierarchy
from projectAndTasks.serializers import TaskSerializer
from taskMgmt.models import Dependency

from django.utils import timezone


def getTasksList(project_id):
    tasks = Task.objects.filter(project_id=project_id).values()
    task_list = []

    for task in tasks:
        # print(task)
        parent_task = TaskHierarchy.objects.filter(sub_task_id=task['id'])
        parent_task_id = 0
        if parent_task.count() == 1:
            parent_task = parent_task.values()[0]
            parent_task_id = parent_task['parent_task_id_id']
            print(parent_task_id)
        t = {
            'id': task['id'],
            'parent_id': parent_task_id,
            'title': task['title'],
            'description': task['description'],
            'creation_date': task['creation_time'],
            'priority': "medium",
            'start': task['start_time'],
            'end': task['end_time'],
            'slack_time': task['slack_time'],
            'category_id': task['category_id_id'],
            'status': task['status']
        }
        task_list.append(t)
    return task_list


def getPredecessorTaskList(task_id_list):
    dependency_list = []
    for task_id in task_id_list:
        predecessor_tasks = Dependency.objects.filter(
            dependent_on_task=task_id).values()
        for predecessor_task in predecessor_tasks:
            t = {
                'id': predecessor_task['id'],
                'predecessor_id': predecessor_task['parent_task_id'],
                'successor_id': task_id
            }
            dependency_list.append(t)
    return dependency_list


def getSubTaskList(task_id):
    subtask_list = []
    subtasks = TaskHierarchy.objects.filter(parent_task_id=task_id).values()

    for subtask in subtasks:
        subtask_id = subtask['sub_task_id_id']
        subtask_info = getTaskDetailsDict(subtask_id)
        subtask_list.append(subtask_info)

    return subtask_list


def getTaskDetailsDict(task_id):
    task_info = Task.objects.filter(id=task_id).values()[0]
    task_dict = {
        'id': task_info['id'],
        'title': task_info['title'],
        'description': task_info['description'],
        'creation_date': task_info['creation_time'],
        'priority': "medium",
        'start': task_info['start_time'],
        'end': task_info['end_time'],
        'slack_time': task_info['slack_time'],
        'category_id': task_info['category_id_id'],
        'status': task_info['status']
    }
    return task_dict

def getRemainingTime(start_date, allocated_time):
    if (allocated_time is None):
        return 0
    # print(type(start_date))
    end_date = start_date+timedelta(days=allocated_time)
    remaining_days = end_date - datetime.now().date()
    # print(end_date, remaining_days)
    return remaining_days.days
    # print(start_date, allocated_time)