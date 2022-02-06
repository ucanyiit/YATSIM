import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from rest_framework.authtoken.models import Token

from yatsim_dashboard.models import Room


class RoomConsumer(JsonWebsocketConsumer):
    groups = [str(room.id) for room in Room.objects.all()]

    def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        token = self.scope["url_route"]["kwargs"]["token"]
        # Join room group
        t = Token.objects.get(key=token)
        user = t.user
        room = Room.objects.get(pk=self.room_id)
        if user in room.guests.all() or user == room.owner:
            print(self.room_id, self.channel_name, "connected")
            self.accept()
            async_to_sync(self.channel_layer.group_add)(self.room_id, self.channel_name)

    def disconnect(self, close_code):
        print("Disconnected")
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(self.room_id, self.channel_name)

    def receive_json(self, json_data):
        """
        Receive message from WebSocket.
        Get the event and send the appropriate event
        """
        print(json_data)

        # if event == 'MOVE':
        #     # Send message to room group
        #     await self.channel_layer.group_send(self.room_group_name, {
        #         'type': 'send_message',
        #         'message': message,
        #         "event": "MOVE"
        #     })

        # if event == 'START':
        #     # Send message to room group
        #     await self.channel_layer.group_send(self.room_group_name, {
        #         'type': 'send_message',
        #         'message': message,
        #         'event': "START"
        #     })

        # if event == 'END':
        #     # Send message to room group
        #     await self.channel_layer.group_send(self.room_group_name, {
        #         'type': 'send_message',
        #         'message': message,
        #         'event': "END"
        #     })

    def send_message(self, res):
        """Receive message from room group"""
        # Send message to WebSocket
        print("res", res)
        self.send_json(res)
