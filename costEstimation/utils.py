from datetime import timedelta
from math import inf
from taskMgmt.utils import totalDaysInCategory, getCategoryTimeMap, timeOfCategoryInRange
from .models import FuncCategory

import scipy.stats

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


def cost_month_graph(all_categories):
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
            "category_time_map": getCategoryTimeMap(category_id=category["id"]),
            "cost": category["misc_cost"] + category["estimated_cost"]
        }

        if start_date == inf:
            start_date = d["category_time_map"][0][0]
            end_date = d["category_time_map"][0][1]
        else:
            start_date = min(start_date, d["category_time_map"][0][0])
            end_date = max(end_date, d["category_time_map"][0][1])

        category_props[str(category["id"])] = d
        

    # print(category_props)
    # print(start_date, end_date)
    
    time_slots = []
    current_date = start_date
    while current_date <= end_date:
        time_slots.append((current_date, current_date + timedelta(days=9)))
        current_date+=timedelta(days=10)
    # print(time_slots)
    # for props in category_props:
    #     start_date = min()

    slot_cost = []

    for time_slot in time_slots:
        time_slot_cost = 0
        for id, category in category_props.items():
            slot_start_date = time_slot[0]
            slot_end_date = time_slot[1]
            id = int(id)
            print(id, category)
            slot_time = timeOfCategoryInRange(slot_start_date, slot_end_date, category["category_time_map"])
            if slot_time == 0:
                continue
            daysTraversed = category["days_traversed"]

            start_cdf = daysTraversed - category["total_days"]/2
            end_cdf = daysTraversed + slot_time - category["total_days"]/2

            sigma = category["total_days"]/6

            category_props[str(id)]["days_traversed"] += slot_time 
            cost = scipy.stats.norm(0, sigma).cdf(end_cdf) - scipy.stats.norm(0, sigma).cdf(start_cdf)
            cost = cost * category["cost"]
            time_slot_cost += cost 
        slot_cost.append(time_slot_cost)

    data = []
    for i in range(len(time_slots)):
        print(time_slots[i], "->", slot_cost[i])
        data.append([time_slots[i][0], time_slots[i][1], slot_cost[i]])

    return data

    
