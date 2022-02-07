from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from rest_framework.authtoken.models import Token

from yatsim_dashboard.models import Room


class RoomConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        token = self.scope["url_route"]["kwargs"]["token"]
        # Join room group
        t = Token.objects.get(key=token)
        user = t.user
        room = Room.objects.get(pk=self.room_id)
        if user in room.guests.all() or user == room.owner:
            self.accept()
            async_to_sync(self.channel_layer.group_add)(self.room_id, self.channel_name)

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(self.room_id, self.channel_name)

    def receive_json(self, json_data):
        print(json_data)

    def send_message(self, res):
        """Receive message from room group"""
        # Send message to WebSocket
        self.send_json(res)
