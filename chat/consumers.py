import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        print("socket is conneted")
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print("socket is disconneted")
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        recipient_id = data['user_id']  # The ID of the user you want to send the message to

        # Send the message to the recipient user
        await self.send_message(recipient_id, message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chatroom_message',
                'message': message,
                #'username': username,
            }
        )
        print("msg is received")
    async def chatroom_message(self, event):
        message = event['message']
        #username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            #'username': username,
        }))

    pass