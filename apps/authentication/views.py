from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import GenericAPIView
from django.contrib.auth import get_user_model
from apps.authentication.serializers import RegistrationSerializer, LoginSerializer
from django.contrib.auth.signals import user_logged_in
from .helpers import success_response
from .backends import generate_api_token


class RegistrationAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request, **kwargs):
        """
        register user
        """
        email, username, password, confirm_passw = request.data.get(
            'email', None
        ), request.data.get('username', None), request.data.get(
            'password', None
        ), request.data.get('confirm_password', None)
        user_data = {
            "email": email,
            "username": username,
            "password": password,
            "confirm_password": confirm_passw
        }
        serializer = self.serializer_class(data=user_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(
            'Acccount created successfully',
            data={
                "username": username,
                "email": email
            },
            status_code=status.HTTP_201_CREATED
        )


class LoginAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.validated_data
        user = get_user_model().objects.get(email=user_data['email'])
        # signal user login
        user_logged_in.send(sender=user, request=request, user=user)
        response_data = {
            "username": user.username,
            "email": user.email,
            "last_login": user.last_login,
            "token": user_data['token']
        }
        return success_response(
            'Login successful',
            data=response_data,
            status_code=status.HTTP_200_OK
        )


class ApiTokenAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        user_data = dict()
        user_data["id"] = request.user.id
        user_data["username"] = request.user.username
        api_token = generate_api_token(user_data)
        response_data = {
            "username": user_data['username'],
            "api_token": api_token
        }
        return success_response(
            'API token obtained successfully',
            data=response_data,
            status_code=status.HTTP_200_OK
        )
