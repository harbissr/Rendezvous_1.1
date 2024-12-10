from django.contrib.auth.password_validation import validate_password
from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.contrib.auth import login, logout, authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import User


# Create your views here.
class Sign_Up(APIView):
    def post(self, request):
        data = request.data.copy()
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            return Response(
                {"error": "Email and password are required."},
                status=HTTP_400_BAD_REQUEST,
            )
        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "A user with this email already exists."},
                status=HTTP_400_BAD_REQUEST,
            )
        try:
            validate_password(password)
        except ValidationError as password_error:
            return Response(
                {"errors": password_error.messages}, status=HTTP_400_BAD_REQUEST
            )
        new_user = User(email=email, username=email)
        new_user.set_password(password)
        try:
            new_user.full_clean()
            new_user.save()
            login(request, new_user)
            token, _ = Token.objects.get_or_create(user=new_user)
            return Response(
                {"user": new_user.email, "token": token.key},
                status=HTTP_201_CREATED,
            )
        except ValidationError as e:
            errors = e.message_dict if hasattr(e, "message_dict") else e.messages
            return Response({"errors": errors}, status=HTTP_400_BAD_REQUEST)


class Log_in(APIView):
    def post(self, request):
        data = request.data.copy()
        email = data.get("email")
        password = data.get("password")
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {"user": user.email, "token": token.key},
                status=HTTP_200_OK,
            )
        return Response(
            {"error": "Invalid email or password."}, status=HTTP_400_BAD_REQUEST
        )


class TokenReq(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class Log_out(TokenReq):
    def post(self, request):
        if hasattr(request.user, "auth_token"):
            request.user.auth_token.delete()
        logout(request)
        return Response(status=HTTP_204_NO_CONTENT)
