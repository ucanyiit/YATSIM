from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Room


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


class DashboardRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = (
            "id",
            "room_name",
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)


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
