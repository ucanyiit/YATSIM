from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Cell, Room, Train, Wagon


class LoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True, allow_blank=False)
    password = serializers.CharField(max_length=150, required=True, allow_blank=False)

    class Meta:
        fields = ("username", "password")


class AuthTokenSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    def get_token(self, obj: Token) -> str:
        return obj.key

    class Meta:
        model = Token
        fields = ("token",)


class RegisterRequestSerializer(serializers.ModelSerializer):
    def validate_password(self, password):
        return password

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])

        user.save()

        return user

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password")
        extra_kwargs = {
            "username": {"required": True, "allow_blank": False},
            "first_name": {"required": True, "allow_blank": False},
            "last_name": {"required": True, "allow_blank": False},
            "email": {"required": True, "allow_blank": False},
            "password": {"required": True, "allow_blank": False},
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)


class DashboardRoomSerializer(serializers.ModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = Room
        depth = 1
        fields = (
            "id",
            "room_name",
            "owner",
        )


class CreateRoomSerializer(serializers.ModelSerializer):
    # owner = UserSerializer() # Nested
    class Meta:
        model = Room
        fields = (
            "room_name",
            "height",
            "width",
            # "owner"
        )


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = (
            "id",
            "room_name",
            "height",
            "width",
        )


class WagonSerializer(serializers.ModelSerializer):
    pass

    class Meta:
        model = Wagon


class CellSerializer(serializers.ModelSerializer):
    pass

    class Meta:
        model = Cell


class TrainSerializer(serializers.ModelSerializer):
    pass

    class Meta:
        model = Train


class DashboardData:
    def __init__(self, user, owned_rooms, guest_rooms):
        self.user = user
        self.owned_rooms = owned_rooms
        self.guest_rooms = guest_rooms


class DashboardSerializer(serializers.Serializer):
    owned_rooms = DashboardRoomSerializer(many=True)
    guest_rooms = DashboardRoomSerializer(many=True)
    user = UserSerializer()

    class Meta:
        fields = ("owned_rooms", "guest_rooms", "username")


class RoomDataSerializer(serializers.Serializer):
    user = UserSerializer()
    room = RoomSerializer()
    cells = CellSerializer(many=True)
    trains = TrainSerializer(many=True)
    running = serializers.BooleanField()

    class Meta:
        fields = ("user", "room", "cells", "trains", "running")


class RoomData:
    def __init__(
        self,
        user,
        room,
        cells,
        trains,
        running,
    ):
        self.user = user
        self.room = room
        self.cells = cells
        self.trains = trains
        self.running = running
