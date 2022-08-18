from django.db import models

from userMgmt.models import User
# from

# Create your models here.


class Notification(models.Model):
    user_sender = models.ForeignKey(
        User,
        null=True, blank=True,
        related_name="user_sender",
        on_delete=models.CASCADE
    )

    user_revoke = models.ForeignKey(
        User,
        null=True, blank=True,
        related_name="user_revoke",
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        default="unread",
    )

    type_of_notification = models.CharField(
        max_length=264, null=True, 
        blank=True
    )


# class TaskComments (models.Model):
#     id = models.AutoField(
#         primary_key=True
#     )

#     task = models.ForeignKey(
#         Task,
#         on_delete=models.CASCADE
#     )

#     comment = models.CharField(
#         max_length=1000,
#         null=False,
#     )
