from projectAndTasks.models import Task
from .utils import getDependencyOfTask
import requests				
from datetime import date, timedelta
# data = {
#     "days_to_start": 13,
#     "dependency": 1,
#     "days_to_end": 22,
#     "on_critical_path": 1,
#     "complexity": 1
# }

BASE_ML_URL = "http://127.0.0.1:8080/api/"

def getDataFromPriorityClass(url, json_data):
    url = BASE_ML_URL + url 
    resp = requests.post(url, json=json_data)

    return resp.json()

def getPriorityOfTask(task_id):
    task = Task.objects.filter(id=task_id).values().first()
    curr_time = date.today()
    data = {
        "days_to_start": max((task["start_time"]-curr_time).days, 0),
        "days_to_end": max((task["end_time"]-curr_time).days, 0),
        "dependency": getDependencyOfTask(task["id"]),
        "complexity": 1,
        "on_critical_path": 1
    }

    text = getDataFromPriorityClass("priority_classifier/predict/", data)
    # print(text, type(text))
    return text["label"], text["point"]