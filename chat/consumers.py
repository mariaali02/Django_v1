import json

from django.contrib.auth.models import User
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        username = data.get('username')  # Separate variable for username
        message = data.get('message')  # Use .get() to safely access the message field
        sender = data.get('sender')  # Use .get() to safely access the message field
        
        # room = data.get('room/room_name')  # Separate variable for the room name

        print("data")
        print(data)
        
        if username and message:
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    
                    'type': 'chat_message',
                    'message': message,
                    'username': username,
                    'sender' : sender,
                }
            )
        else:
            # Handle missing or incomplete data
            print("Invalid or incomplete data received.")
    
    async def sendMessage(self , event) :
        message = event["message"]
        username = event["username"]
        sender = event["sender"]
        
        await self.send(text_data = json.dumps({"sender" : sender , "message":message ,"username":username}))
        print(0)
    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        sender = event["sender"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'sender': sender
        }))

