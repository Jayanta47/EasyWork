from datetime import datetime, timedelta, date
from math import inf
from costEstimation.models import FuncCategory
from costEstimation.serializers import FuncCategorySerializer
from projectAndTasks.models import Project, Task, TaskHierarchy, User_Project_Map, Project_Category_Map
from projectAndTasks.serializers import ProjectSerializer, TaskSerializer
from taskMgmt.models import Dependency, User_Task_Map, Milestones
from userMgmt.models import User, Designation
from costEstimation.models import FuncCategory

from django.db.models import Q

import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import random
import string
from easywork_be.settings import MEDIA_ROOT


def getTasksList(project_id):
    tasks = Task.objects.filter(project_id=project_id).values()
    task_list = []

    for task in tasks:
        # print(task)
        parent_task = TaskHierarchy.objects.filter(sub_task_id=task['id'])
        milestone = Milestones.objects.filter(task=task['id']).values()
        if len(milestone) > 0:
            milestone = True
        else:
            milestone = False
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
            'status': task['status'],
            'milestone': milestone
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


# get the duration of a task given its id
def getTaskDuration(task_id):
    task = Task.objects.filter(id=task_id).values("start_time", "end_time").first()
    return max(0, (task["end_time"] - task["start_time"]).days)

def getTaskTitle(task_id):
    task = Task.objects.filter(id=task_id).values("title").first()
    return task["title"]

def getPredGraphList(task_id_list):
    pred_list = []
    ac_list = []
    duration_list = []
    sorted(task_id_list)

    map = {}

    for i in range(len(task_id_list)):
        task_id = task_id_list[i]
        name=""
        while task_id > 0:
            j = task_id%26
            task_id = task_id // 26
            name+=chr(ord('A')+j-1)

        title = getTaskTitle(task_id_list[i])
        ac_list.append(name)
        map[str(task_id_list[i])] = [name, title]

    # print(map)

    for task_id in task_id_list:
        predecessor_tasks = Dependency.objects.filter(
            dependent_on_task=task_id).values()
        dependency_str = ""
        if len(predecessor_tasks) == 0:
            dependency_str = "-"
        else:
            for predecessor_task in predecessor_tasks:
                predecessor_id = predecessor_task['parent_task_id']
                if predecessor_id in task_id_list:
                    dependency_str+=chr(ord('A')+predecessor_id-1)

        pred_list.append(dependency_str)
        duration_list.append(getTaskDuration(task_id))

    # print("ac_list", ac_list)
    # print("predlist", pred_list)
    return map, task_id_list, ac_list, pred_list, duration_list

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
        wage = 0
        weekly_effort = 0
        for m in all_user_maps:
            wage = max(m['wage'], wage)
            weekly_effort = max(m['weekly_effort'], weekly_effort)
            user = User.objects.filter(id=m["user_id_id"]).values()[0]
            job_id = user['job_id']
            job = Designation.objects.filter(id=job_id).values()[0]["job_name"]
            if str(job) in all_categories:
                all_categories[str(job)]["count"] = all_categories[str(job)]["count"] + 1
                all_categories[str(job)]["users"].append(user["id"])
            else:
                all_categories[str(job)]= {"count": 1, "users": [user["id"]], "wage":wage, "weekly_effort": weekly_effort}

    final_data = []
    for key, value in all_categories.items():
        d = {
            "post": key,
            "count": value["count"],
            "users": value["users"],
            "wage": value["wage"],
            "weekly_effort": value["weekly_effort"],
        }
        final_data.append(d)

    return final_data

def getAllMembersOfProject(project_id):
    tasks = Task.objects.filter(project_id=project_id).values()
    all_categories = {}
    for task in tasks:
        all_user_maps = User_Task_Map.objects.filter(
            task_id=task['id']).values()
        wage = 0
        weekly_effort = 0
        for m in all_user_maps:
            wage = max(m['wage'], wage)
            weekly_effort = max(m['weekly_effort'], weekly_effort)
            user = User.objects.filter(id=m["user_id_id"]).values()[0]
            job_id = user['job_id']
            job = Designation.objects.filter(id=job_id).values()[0]["job_name"]
            if str(job) in all_categories:
                all_categories[str(job)]["count"] = all_categories[str(job)]["count"] + 1
                all_categories[str(job)]["users"].append(user["id"])
            else:
                all_categories[str(job)]= {"count": 1, "users": [user["id"]], "wage":wage, "weekly_effort": weekly_effort}

    final_data = []
    for key, value in all_categories.items():
        d = {
            "post": key,
            "count": value["count"],
            "users": value["users"],
            "wage": value["wage"],
            "weekly_effort": value["weekly_effort"],
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


def generateRandomString(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str



def generateDependencyGraph(ancestry):
    start = []
    graph = []
    atts = []
    path = []
    new = []
    st = ""
    # data = pd.read_csv("data/data"+str(q)+".csv")
    data = pd.DataFrame(ancestry)
    last = data.iloc[-1, 0]
    last = chr(ord(last)+1)
    # -------------------------------------------
    for j in range(len(data)):
        for k in range(len(data.iloc[j, 1])):
            if data.iloc[j, 1][k] != '-':
                new.append(data.iloc[j, 1][k])
    # -------------------------------------------
    for j in range(len(data)):
        if not data.iloc[j, 0] in new:
            st = st+data.iloc[j, 0]
    # ------------------------------------------
    if data.shape[1] == 3:
        df = pd.DataFrame([[last, st, 0]], columns=["ac", "pr", "du"])
    else:
        df = pd.DataFrame([[last, st, 0, 0, 0]], columns=[
                        "ac", "pr", "b", "m", "a"])
    data = pd.concat([data, df]) #data.append(df)
    for i in range(len(data)):
        graph.append([])
        atts.append({})
    for j in range(len(data)):
        atts[j]["Name"] = data.iloc[j, 0]
        if data.shape[1] == 3:
            atts[j]["DU"] = data.iloc[j, 2]
        else:
            atts[j]["DU"] = (data.iloc[j, 4] + 4 *
                            data.iloc[j, 3] + data.iloc[j, 2]) / 6
        if(data.iloc[j, 1] == "-"):
            start.append(ord(data.iloc[j, 0])-65)
            continue
        for k in range(len(data.iloc[j, 1])):
            graph[ord(data.iloc[j, 1][k]) -
                65].append(ord(data.iloc[j, 0])-65)

    level = [None] * (len(graph))


    # BFS
    s = start.copy()
    visited = [False] * (len(graph))
    queue = []
    for i in s:
        queue.append(i)
        level[i] = 0
        visited[i] = True
    while queue:
        s = queue.pop(0)
        path.append(s)
        for i in graph[s]:
            if visited[i] == False:
                queue.append(i)
                level[i] = level[s] + 1
                visited[i] = True
            else:
                level[i] = max(level[s]+1, level[i])

    levels = [None] * len(path)
    for i in range(len(path)):
        levels[i] = level[path[i]]
    path = [x for y, x in sorted(zip(levels, path))]
    # print()
    # print("Path")
    for i in path:
        print(str(chr(i+65)), end=' ')
    for s in path:
        # print(str(chr(s+65)), " ", level[s])
        # -------------Forward--------------------
        if(data.iloc[s, 1] == "-"):
            atts[s]["ES"] = 0
        else:
            ls = []
            for k in range(len(data.iloc[s, 1])):
                ls.append(atts[ord(data.iloc[s, 1][k]) - 65]["EF"])
            atts[s]["ES"] = max(ls)
        atts[s]["EF"] = atts[s]["DU"] + atts[s]["ES"]
        # ---------------------------------

    for i in range(len(graph)):
        if(graph[i] == []):
            atts[i]["LF"] = atts[i]["EF"]
            atts[i]["LS"] = atts[i]["ES"]
    # print()
    # print("------------------------")
    # --------------------backward
    path.reverse()
    for i in path:
        if(data.iloc[i, 1] != "-"):
            for k in range(len(data.iloc[i, 1])):
                if "LF" in atts[ord(data.iloc[i, 1][k]) - 65].keys():
                    atts[ord(data.iloc[i, 1][k]) - 65]["LF"] = min(atts[i]
                                                                ["LS"], atts[ord(data.iloc[i, 1][k]) - 65]["LF"])
                else:
                    atts[ord(data.iloc[i, 1][k]) -
                        65]["LF"] = atts[i]["LS"]
                atts[ord(data.iloc[i, 1][k]) - 65]["LS"] = atts[ord(data.iloc[i, 1]
                                                                    [k]) - 65]["LF"] - atts[ord(data.iloc[i, 1][k]) - 65]["DU"]
        atts[i]["SK"] = atts[i]["LF"] - atts[i]["EF"]
    # ----------------------------------------
    atts[-1]["Name"] = "End"
    # atts.pop()


    ###  print here ###########
    # for j in range(len(graph)):
    #     print(atts[j])
    # print()
    # ------------------------------------------------
    G2 = nx.DiGraph()

    for i in range(len(graph)):
        for j in graph[i]:
            G2.add_edge(atts[i]["Name"], atts[j]["Name"])
    temp = []
    for i in range(len(atts)):
        temp.append(atts[i]["Name"])
    temp = dict(zip(temp, atts))
    nx.set_node_attributes(G2, temp)
    fig, ax = plt.subplots(figsize=(15, 15))
    pos = nx.nx_agraph.graphviz_layout(G2, prog='dot')
    # nx.draw(G2, pos=pos, ax=ax, with_labels=True, font_weight='bold')
    nx.draw_networkx_edges(G2, pos, edge_color='olive',
                        width=1, arrowstyle='simple', arrowsize=20, min_source_margin=25, min_target_margin=25)
    crt = []
    notcrt = []
    for j, i in temp.items():
        if(i["LF"] == i["EF"]):
            crt.append(j)
        else:
            notcrt.append(j)
    nx.draw_networkx_nodes(G2, pos, node_size=2000,
                        node_color='seagreen', ax=ax, nodelist=crt)
    nx.draw_networkx_nodes(G2, pos, node_size=1000,
                        node_color='wheat', ax=ax, nodelist=notcrt)
    nx.draw_networkx_labels(G2, pos, ax=ax, font_weight="bold",
                            font_color="black", font_size=16)

    def without(d, keys={"Name"}):
        return {x: d[x] for x in d if x not in keys}
    for node in G2.nodes:
        xy = pos[node]
        node_attr = G2.nodes[node]
        d = G2.nodes[node]
        d = without(d)
        text = '\n'.join(f'{k}: {v}' for k,
                        v in d.items())
        ax.annotate(text, xy=xy, xytext=(50, 5), textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="lightgrey"),
                    arrowprops=dict(arrowstyle="wedge"))
    ax.axis('off')
    fig_name = "fig_"+generateRandomString(10)+".png"
    plt.savefig(MEDIA_ROOT+"/"+ fig_name)

    return fig_name, atts



def getUserTaskList(project_id, user_id):
    all_user_tasks = User_Task_Map.objects.filter(user_id=user_id).values()
    selected_tasks = []
    for ut_map in all_user_tasks:
        task_id = ut_map['task_id_id']
        task = Task.objects.filter(id=task_id, project_id=project_id).values()
        if len(task) != 0:
            selected_tasks.append(task[0])

    return selected_tasks


def getUserSubTaskList(task_id, user_id):
    all_user_tasks = User_Task_Map.objects.filter(user_id=user_id).values()
    selected_tasks = []
    for ut_map in all_user_tasks:
        task_id = ut_map['task_id_id']
        subtask_list = TaskHierarchy.objects.filter(parent_task_id__id = task_id).values()
        if len(subtask_list) != 0:
            for subtask in subtask_list:
                subtask_id = subtask["id"]
                task = Task.objects.filter(task_id=subtask_id).values().first()
                selected_tasks.append(task)

    return selected_tasks

def updateTaskMapForUserAndCat(category_id, user_id, effort, wage):
    task_in_cat_list = Task.objects.filter(category_id=category_id).values()
    user_task_list = []
    for task in task_in_cat_list:
        task_id = task['id']
        user_task_map = User_Task_Map.objects.filter(task_id=task_id, user_id=user_id).values('id')
        if len(user_task_map) > 0:
            user_task_map_id = user_task_map[0]['id']
            User_Task_Map.objects.filter(id=user_task_map_id).update(weekly_effort=effort, wage=wage)


def getDependencyOfTask(task_id):
    return Dependency.objects.filter(parent_task__id=task_id).count()


def calculateTotalCostAndBudgetOfProject(project_id):
    all_func_categories_map = Project_Category_Map.objects.filter(project_id = project_id)

    total_cost = 0
    total_budget = 0
    for func_category_map in all_func_categories_map:
        category = func_category_map.category

        serializer = FuncCategorySerializer(category)
        total_cost += (serializer.data["estimated_cost"] + serializer.data["  misc_cost"])
        total_budget += (serializer.data["allocated_budget"])

    return total_budget, total_cost



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
