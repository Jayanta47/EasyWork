from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from rest_framework import generics

from costEstimation.utils import cost_month_graph
# from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin

from .models import FuncCategory
from taskMgmt.utils import getAllMembersOfCategory, getAllTasksOfCategory, updateTaskFuncCategory
from taskMgmt.utils import getCategoriesUnderProject, getUnCategorisedTasks, addProjectCategoryMap, updateTaskMapForUserAndCat
from .serializers import FuncCategorySerializer

from .cocomoii import *


@api_view(["GET"])
def getCategoryData(request, cat_id):
    category = FuncCategory.objects.filter(id=cat_id).values()
    if len(category) > 0:
        category = category[0]
        all_members = getAllMembersOfCategory(cat_id=cat_id)
        category["allocated_members"] = all_members
        # d = {
        #     "category_name": category['title'],
        #     "expected_time": category['expected_time'],
        #     "allocated_budget": category['allocated_budget'],
        #     "man_hour_per_week": category['man_hour_per_week'],
        #     "allocated_budget": category['allocated_budget'],
        #     "allocated_members": all_members,
        # }

        return Response({"success": True, "data": category},
                        status=status.HTTP_200_OK)
    else:
        return Response({"success": False},
                        status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def getAllCategorySummary(request, project_id):
    d = []

    all_categories = getCategoriesUnderProject(project_id)
    # print(all_categories)

    for category in all_categories:
        # print(category)
        members = getAllMembersOfCategory(cat_id=category['id'])
        # people_assigned = len(members)
        all_tasks = getAllTasksOfCategory(cat_id=category['id'])
        d_ = {
            "id": category['id'],
            "category_name": category['title'],
            "expected_time": category['expected_time'],
            "allocated_budget": category['allocated_budget'],
            "man_hour_per_week": category['man_hour_per_week'],
            "allocated_members": len(members),
            "total_task": len(all_tasks)
        }
        d.append(d_.copy())
    return Response({"success": True, "data": d},
                    status=status.HTTP_200_OK)


@api_view(["GET"])
def getAllCategoryWithTaskName(request, project_id):
    data = []
    all_categories = getCategoriesUnderProject(project_id)

    for category in all_categories:
        print(category)
        all_tasks = getAllTasksOfCategory(cat_id=category['id'])
        # print("tasks", all_tasks)

        category_data = {
            "id": category["id"],
            "title": category["title"],
            "tasks": all_tasks
        }

        data.append(category_data)
    # print(data)

    uncategorised_tasks = getUnCategorisedTasks(project_id) # returns list of dict

    category_data = {
        "id": 0,
        "title": "Unlisted",
        "tasks": uncategorised_tasks
    }

    data.append(category_data)

    return Response({"success": True, "data": data},
                    status=status.HTTP_200_OK)


@api_view(["POST"])
def setDecomposition(request):
    data = request.data["data"]

    for category_data in data:
        tasks = category_data["tasks"]
        for task in tasks:
            updateTaskFuncCategory(task["id"], category_data["id"])

    deletion_list = request.data["toDelete"]

    for category_id in deletion_list:
        FuncCategory.objects.filter(id=category_id).delete()

    return Response({"success": True}, status=status.HTTP_200_OK)


@api_view(["POST"])
def editCategories(request):
    project_id = request.data['project_id']
    category_create_list = request.data['toCreate']
    new_category_list = []
    for new_category_title in category_create_list:
        funcSerializer = FuncCategorySerializer(
            data={"title": new_category_title})
        if funcSerializer.is_valid():
            funcSerializer.save()
            print(funcSerializer.data)
            addProjectCategoryMap(project_id, funcSerializer.data['id'])
            new_category_list.append(funcSerializer.data)

    category_modify_list = request.data['toModify']

    for category_data in category_modify_list:
        funcData = FuncCategory.objects.get(id=category_data['id'])
        # print(funcData)
        funcSerializer = FuncCategorySerializer(funcData, data=category_data)
        if funcSerializer.is_valid():
            funcSerializer.save()

    return Response({"success": True}, status=status.HTTP_200_OK)


class UpdateFuncCategory(generics.UpdateAPIView):
    queryset = FuncCategory.objects.all()

    serializer_class = FuncCategorySerializer


@api_view(["POST"])
def getCostMonthGraph(request):
    data = request.data
    project_id = data['project_id']
    if data["all"]==True:
        all_categories = getCategoriesUnderProject(project_id)
    else:
        all_categories = FuncCategory.objects.filter(id=data["category_id"]).values()
    print(all_categories)
    data = cost_month_graph(all_categories)
    return Response({"success": True, "data": data}, status=status.HTTP_200_OK)


@api_view(["POST"])
def updateUserTaskMap(request):
    data = request.data
    category_id = data["category_id"]
    user_list = data["users"]

    for user in user_list:
        updateTaskMapForUserAndCat(category_id, user['user_id'], user['effort'], user['wage'])

    # print(data)

    return Response({"success": True}, status=status.HTTP_200_OK)

# class DeleteFuncCategory(generics.DestroyAPIView):
#     queryset = FuncCategory.objects.all()
#     serializer_class = FuncCategorySerializer

@api_view(["POST"])
def calculateCostAdvanced(request):
    data = request.data

    # PREC
    # FLEX
    # RESL
    # TEAM
    # PMAT

    # architectureRiskResolution - RESL 
    # developmentFlexibility - FLEX 
    # precedentedness - PREC 
    # processMaturity - PMAT 
    # teamCohesion - TEAM 

    scale_factor_list = [
        int(data["precedentedness"]),
        int(data["developmentFlexibility"]),
        int(data["architectureRiskResolution"]),
        int(data["teamCohesion"]),
        int(data["processMaturity"])
    ]

    # modifiedAssessmentAndAssimilation - 
    # modifiedCodeModified - 
    # modifiedDesignModifed - 
    # modifiedIntegrationRequired - 
    # modifiedSLOC - 
    # modifiedSoftwareUnderstanding - 
    # modifiedUnfamiliarity - 
    # newSLOC - 
    # reusedAssessmentAndAssimilation - 
    # reusedIntegrationRequired - 
    # reusedSLOC - 

    # analystCapability - ACAP
    # applicationExperience - APEX
    # dataBaseSize - DATA 
    # developedForReusability - RUSE
    # documentationMatchToLifecycleNeeds - DOCU
    # languageAndToolsetExperience - LTEX
    # multisiteDevelopment - SITE
    # personnelContinuity - PCON
    # platformExperience - PLEX
    # platformVolatility - PVOL
    # productComplexity - CPLX
    # programmerCapability - PCAP
    # requiredDevelopmentSchedule - SCED
    # requiredSoftwareReliability - RELY
    # storageConstraint - STOR
    # timeConstraint - TIME
    # useOfSoftwareTools - TOOL

    effortM_level_dict = {
        "RELY_level": int(data["requiredSoftwareReliability"]),
        "DATA_level": int(data["dataBaseSize"]),
        "CPLX_level": int(data["productComplexity"]),
        "RUSE_level": int(data["developedForReusability"]),
        "DOCU_level": int(data["documentationMatchToLifecycleNeeds"]),
        "TIME_level": int(data["timeConstraint"]),
        "STOR_level": int(data["storageConstraint"]),
        "PVOL_level": int(data["platformVolatility"]),
        "ACAP_level": int(data["analystCapability"]),
        "PCAP_level": int(data["programmerCapability"]),
        "PCON_level": int(data["personnelContinuity"]),
        "APEX_level": int(data["applicationExperience"]),
        "PLEX_level": int(data["platformExperience"]),
        "LTEX_level": int(data["languageAndToolsetExperience"]),
        "TOOL_level": int(data["useOfSoftwareTools"]),
        "SITE_level": int(data["multisiteDevelopment"]),
        "SCED_level": int(data["requiredDevelopmentSchedule"]),
    }

    SLOC = int(data["newSLOC"]) + int(data["reusedSLOC"]) * (int(data["reusedIntegrationRequired"])*0.8 + int(data["reusedAssessmentAndAssimilation"]))
    SLOC += int(data["modifiedSLOC"])*(0.2+int(data["modifiedDesignModifed"])*0.5+int(data["modifiedCodeModified"])*0.6+int(data["modifiedSoftwareUnderstanding"])*0.1+int(data["modifiedUnfamiliarity"]*0.1))

    effort = calculateEffort(scale_factor_list, effortM_level_dict, SLOC)
    time = calculateTime(effort=effort)
    devCost = calculateDevCost

    return Response({"success": True, "effort": effort, "time": time, "devCost": devCost}, status=status.HTTP_200_OK)
