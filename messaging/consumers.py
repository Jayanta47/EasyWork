import json 
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class NotificationConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        
        return await super().connect(self)