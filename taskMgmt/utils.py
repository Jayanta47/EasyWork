from datetime import datetime, timedelta, date
from math import inf
from unicodedata import category
from costEstimation.models import FuncCategory
from projectAndTasks.models import Project, Task, TaskHierarchy, User_Project_Map, Project_Category_Map
from projectAndTasks.serializers import TaskSerializer
from taskMgmt.models import Dependency, User_Task_Map
from userMgmt.models import User, Designation
from costEstimation.models import FuncCategory

from django.utils import timezone
from django.db.models import Q


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
                'dependency_id': predecessor_task['id'],
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


def getAllMembersOfCategory(cat_id):
    tasks = Task.objects.filter(category_id=cat_id).values()
    all_categories = {}
    for task in tasks:
        all_user_maps = User_Task_Map.objects.filter(
            task_id=task['id']).values()

        for m in all_user_maps:
            user = User.objects.filter(id=m["user_id_id"]).values()[0]
            job_id = user['job_id']
            job = Designation.objects.filter(id=job_id).values()[0]["job_name"]
            if str(job) in all_categories:
                all_categories[str(job)]["count"] = all_categories[str(job)]["count"] + 1
                all_categories[str(job)]["users"].append(user["id"])
            else:
                all_categories[str(job)]= {"count": 1, "users": [ user["id"] ]}

    final_data = []
    for key, value in all_categories.items():
        d = {
            "post": key,
            "count": value["count"],
            "users": value["users"]
        }
        final_data.append(d)

    return final_data


def getAllTasksOfCategory(cat_id):
    tasks = Task.objects.filter(category_id=cat_id).values()
    task_list = []
    for task in tasks:
        d = {

            "id": task["id"],
            "title": task["title"]
        }
        task_list.append(d)
    return task_list


def updateTaskFuncCategory(task_id, new_cat_id):

    # print('done', task_id, new_cat_id)
    if new_cat_id != 0:
        Task.objects.filter(id=task_id).update(category_id_id=new_cat_id)
    else:
        Task.objects.filter(id=task_id).update(category_id=None)
    # task.update(category_id_id=new_cat_id)


def getCategoriesUnderProject(project_id):
    all_project_category_map = Project_Category_Map.objects.filter(
        project=project_id).values()
    all_categories = []
    for project_category_map in all_project_category_map:
        category = FuncCategory.objects.filter(
            id=project_category_map['category_id']).values()[0]
        all_categories.append(category)
    return all_categories


def getUnCategorisedTasks(project_id):
    tasks = Task.objects.filter(
        Q(project_id=project_id) & Q(category_id__isnull=True)
    ).values()

    task_list = []
    for task in tasks:
        d = {

            "id": task["id"],
            "title": task["title"]
        }
        task_list.append(d)
    return task_list


def addProjectCategoryMap(project_id, category_id):
    t = Project_Category_Map.objects.create(
        project_id=project_id, category_id=category_id)


def totalDaysInCategory(category_id):
    all_tasks = Task.objects.filter(category_id=category_id).values()

    return totalDurationOfTasks(all_tasks=all_tasks)

def totalDaysInProject(project_id):
    all_tasks = Task.objects.filter(project_id=project_id).values()

    return totalDurationOfTasks(all_tasks=all_tasks)

def totalDurationOfTasks(all_tasks):
    curr_time = date.today()
    task_start_end_list = []
    for task in all_tasks:
        start_date = task["start_time"]
        end_date = task["end_time"]
        task_start_end_list.append(
            (task['id'], (start_date-curr_time).days, (end_date-curr_time).days))

    task_start_end_list = sorted(task_start_end_list, key=lambda x: x[2])
    
    # print(task_start_end_list)
    total_duration = 0

    last_finishing_time = -inf

    for x in task_start_end_list:
        if last_finishing_time < x[1]:
            total_duration = total_duration + (x[2]-x[1])+1
        else:
            total_duration = total_duration + x[2] - last_finishing_time+1
        last_finishing_time = x[2]

    return total_duration




def getCategoryTimeMap(category_id):
    all_tasks = Task.objects.filter(category_id=category_id).values()

    return getTaskListTimeMap(all_tasks)


def timeOfCategoryInRange(start_date, end_date, time_map):
    total_time = 0

    for time_interval in time_map:
        start = max(time_interval[0], start_date)
        end = min(time_interval[1], end_date)

        days = (end-start).days
        if days < 0:
            total_time += 0
        else:
            total_time += days 
    
    return total_time

def getTaskListTimeMap(task_list):
    task_start_end_list = []
    time_map = []

    if len(task_list) == 0:
        return time_map
    for task in task_list:
        start_date = task["start_time"]
        end_date = task["end_time"]
        task_start_end_list.append(
            (task['id'], start_date, end_date))

    task_start_end_list = sorted(task_start_end_list, key=lambda x: x[1])

    # print(task_start_end_list)

    current_segment_start_date = task_start_end_list[0][1]
    current_segment_end_date = task_start_end_list[0][2]
    
    for x in task_start_end_list:
        end_date = x[2]
        start_date = x[1]

        if current_segment_end_date < start_date:
            segment_tuple = (current_segment_start_date, current_segment_end_date)
            time_map.append(segment_tuple)
            current_segment_start_date = start_date
            current_segment_end_date = end_date
        else:
            current_segment_end_date = max(end_date, current_segment_end_date)

    time_map.append((current_segment_start_date, current_segment_end_date))

    # print(time_map)
    return time_map

# error in implementation


# def getAllMembersOfCategory(cat_id):
#     tasks = Task.objects.filter(category_id=cat_id).values()[0]
#     if tasks is not None:
#         project_id = tasks["project_id_id"]
#     print("project_id", project_id)
#     all_maps = User_Project_Map.objects.filter(project_id=project_id).values()
#     all_categories = {}

#     for m in all_maps:
#         user = User.objects.filter(id=m["user_id_id"]).values()[0]
#         job_id = user['job_id']
#         job = Designation.objects.filter(id=job_id).values()[0]["job_name"]
#         if str(job) in all_categories:
#             all_categories[str(job)] = all_categories[str(job)] + 1
#         else:
#             all_categories[str(job)] = 1
#     # print(all_categories)

#     final_data = []
#     for key, value in all_categories.items():
#         d = {
#             "post": key,
#             "count": value
#         }
#         final_data.append(d)

#     return final_data
