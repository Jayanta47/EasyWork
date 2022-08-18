import json
from sqlite3 import connect 
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

from asgiref.sync import async_to_sync,sync_to_async

from .models import Notification
from userMgmt.models import User

@database_sync_to_async
def create_notificaton(receiver, type_of="task_created", status="unread"):
    notification_to_create = Notification.objects.create(user_revoker=receiver,
                type_of_notification=type_of)
    print('I am here to help')
    return (notification_to_create.user_revoker.id, notification_to_create.type_of_notification)


@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.filter(id=user_id).first()
    except:
        print("User Not found")



class NotificationConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        # print('connected', event)
        
        await self.accept()
        await self.send(json.dumps({
            "type":"websocket.send",
            "text":"hello world"
        }))

        self.group_name = "messaging"

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        self.send({
            "type":"websocket.send",
            "text":"room made"
        })

    async def disconnect(self):
        # leave group 
        await self.channel_layer.group_discard(self.group_name, self.channel_name)


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        message = text_data_json["message"]
        user_id = text_data_json["user_id"]

        receiver = await get_user(user_id)
        print(receiver)

        create_notificaton(receiver)

        event = {
            'type': 'send_message',
            'message': message
        }

        await self.channel_layer.group_send(self.group_name, event)

    async def send_message(self, event):

        message = event["message"]

        await self.send(text_data=json.dumps({"message": message}))
        
       