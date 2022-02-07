from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import User

from .models import Cell, Train
from .serializers import CellSerializer, TrainSerializer, UserSerializer


def send_user_data(guests, room_id, user):
    users = User.objects.exclude(id__exact=user.id).exclude(
        id__in=[user.id for user in guests.all()]
    )
    users_data = UserSerializer(users, many=True)
    guests_data = UserSerializer(guests, many=True)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        str(room_id),
        {
            "type": "send_message",
            "event": "users",
            "users": users_data.data,
            "guests": guests_data.data,
        },
    )


def send_trains_data(room_id):
    trains = Train.objects.filter(room_id__exact=room_id)
    trains_data = TrainSerializer(trains, many=True)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        str(room_id),
        {
            "type": "send_message",
            "event": "trains",
            "trains": trains_data.data,
        },
    )


def send_cells_data(room_id):
    cells = Cell.objects.filter(room_id__exact=room_id)
    cells_data = CellSerializer(cells, many=True)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        str(room_id),
        {"type": "send_message", "event": "cell_change", "cells": cells_data.data},
    )
