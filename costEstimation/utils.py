from datetime import timedelta
from math import inf
from taskMgmt.utils import totalDaysInCategory, getCategoryTimeMap, timeOfCategoryInRange
from .models import FuncCategory

def estimateEffort(loc, task_level, months):
    if task_level == "easy":
        p = 2000
    elif task_level == "medium":
        p = 10000
    elif task_level == "hard":
        p = 20000
    else:
        raise Exception("invalid task difficulty")

    if loc < 15E3:
        B = 0.16
    else:
        B = 0.39

    return (loc/p)**3 * B * months**-4


def cost_month_graph():
    all_categories = FuncCategory.objects.all().values()

    category_props = {}

    start_date = inf
    end_date = inf 

    for category in all_categories:
        d = {
            "title": category["title"],
            "days_traversed": 0,
            "total_days": totalDaysInCategory(category_id=category["id"]),
            "type": "normal",
            "category_time_map": getCategoryTimeMap(category_id=category["id"])
        }

        if start_date == inf:
            start_date = d["category_time_map"][0][0]
            end_date = d["category_time_map"][0][1]
        else:
            start_date = min(start_date, d["category_time_map"][0][0])
            end_date = max(end_date, d["category_time_map"][0][1])

        category_props[str(category["id"])] = d
        

    print(category_props)
    print(start_date, end_date)
    
    time_slots = []
    current_date = start_date
    while current_date <= end_date:
        time_slots.append((current_date, current_date + timedelta(days=9)))
        current_date+=timedelta(days=10)
    print(time_slots)
    # for props in category_props:
    #     start_date = min()