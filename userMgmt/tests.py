from unicodedata import decomposition
from django.test import TestCase

# Create your tests here.

# 127.0.0.1:8000/user/getallusers/

# 127.0.0.1:8000/project/getproject/4

# 127.0.0.1:8000/taskmgmt/getproject_tasks/

# 127.0.0.1:8000/taskmgmt/gettaskdetails/


# adding a project to the db 

# url: 127.0.0.1:8000/project/addproject/

# data:
# {
#     "title":"Project2",
#     "description": "description for the second project",
#     "allocated_time": 50,
#     "budget": 2000,
#     "dev_type": "Not specified"
# }

# adding a task to the db 

# url: 127.0.0.1:8000/project/addtask/

# data:
# {
#     "project_id":5,
#     "title": "Task1",
#     "description": "Task 1 description for project2",
#     "start_time": "2022-07-18",
#     "end_time": "2022-08-18",
#     "status": "Not Started" #optional, "Not Started" by default
#     "slack_time": 2, # optional, default 0
#     "category_id": 1 #optional, default null
# }

# adding a comment

# url: 127.0.0.1:8000/project/addcomments/

# data:
# {
#     "task": 3,
#     "comment": "You can delay this for 2 days"
# }

# getting a comment 

# url: 127.0.0.1:8000/project/getcomments/

# {
#     "task_id": 3
# }

# adding hierarchy 
# url : 127.0.0.1:8000/project/addtaskparent/

# data:

# {
#     "parent_task_id": 1,
#     "sub_task_id": 2
# }

# editing decomposition

# url: 127.0.0.1:8000/costEstm/editCategories/

# data:

# {
#     "toCreate": ["new func 3", "new func 4"],
#     "toModify": [
#         {
#             "id": 1,
#             "title": "modified 1"
#         }
#     ] 
# }

# set decomposition

# url: 127.0.0.1:8000/costEstm/setDecomposition/

# data:

# {
#     "data": [
#         {
#             "id":13,
#             "tasks": [
#                 {
#                     "id":3
#                 },
#                 {
#                     "id":6
#                 }
#             ]
#         }
#     ],
#     "toDelete": [14] 
# }

# update user

# url: 127.0.0.1:8000/user/updateUser/2/

# data:
# {
#     "first_name": "Jayanta",
#     "last_name": "Sadhu",
#     "date_of_birth": "1999-02-17",
#     "gender": "M"
# }