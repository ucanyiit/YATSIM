# from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import CreateAPIView

# from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response

from .serializers import (
    AuthTokenSerializer,
    LoginRequestSerializer,
    RegisterRequestSerializer,
)

# TODO: There are some empty control flow branches (else: pass). Let's have
# a look at them.

# pylint:disable=w0702
# TODO: Bare exceptions. What are possible exceptions and how to resolve them?
# Implement a robusts checking mechanism.


class LoginAPIView(APIView):
    """
    Login endpoint for users
    The username field accepts both usernames and emails
    """

    def post(self, request):
        serializer = LoginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        profile = User.objects.filter(username=serializer.validated_data["username"]).first()

        if profile is None or not profile.check_password(
            serializer.validated_data["password"]
        ):
            raise AuthenticationFailed()

        try:
            auth_token = Token.objects.get(user=profile)
        except:
            auth_token = Token.objects.create(user=profile)

        return Response(AuthTokenSerializer(auth_token).data)


class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterRequestSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user: User = serializer.save()

        user.is_active = True  # TODO: disable later, just for testing purposes
        user.save()

        return user
