import json
import os
import random
import secrets
import string

import requests
from django.core.cache import cache
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from authorization.mixins.auth import BaseAuthenticatedMixin
from authorization.models import CustomUser
from authorization.serializers import EmailSerializer, EmailCodeSerializer, GoogleOAuthSerializer, YandexOAuthSerializer, SendCodePhoneSerializer, \
    ValidateCodePhoneSerializer
from utils.sms import send_code, send_password


class ResetPasswordSendCodeView(generics.GenericAPIView):
    serializer_class = EmailSerializer

    def post(self, request, *args, **kwargs):
        validated_data = self.serializer_class(data=request.data)
        validated_data.is_valid(raise_exception=True)
        serialized_data = validated_data.validated_data
        user = get_object_or_404(CustomUser, email=serialized_data["email"])
        code = ''.join(random.choices(string.digits, k=6))
        cache.set(user.email, code, 900)
        send_code(serialized_data["email"], code)
        return Response(status=200)


class ResetPasswordEmailView(generics.GenericAPIView):
    serializer_class = EmailCodeSerializer

    def post(self, request, *args, **kwargs):
        validated_data = self.serializer_class(data=request.data)
        validated_data.is_valid(raise_exception=True)
        serialized_data = validated_data.validated_data
        user = get_object_or_404(CustomUser, email=serialized_data["email"])
        if cache.get(user.email) != serialized_data["code"]:
            return Response(status=400)

        password = secrets.token_urlsafe(6)
        user.set_password(password)
        user.save()
        send_password(user.email, password)
        return Response(status=200)


class GoogleOauthView(generics.CreateAPIView):
    serializer_class = GoogleOAuthSerializer

    def create(self, request, *args, **kwargs):
        serializing = self.serializer_class(data=request.data)
        serializing.is_valid(raise_exception=True)
        validated_data = serializing.validated_data

        response = requests.post(os.getenv("GOOGLE_OAUTH"), params=validated_data)
        data = response.json()
        try:
            user = CustomUser.objects.create(email=data.get("email"),
                                             first_name=data.get("given_name", ""),
                                             last_name=data.get("family_name", ""),
                                             phone_number="",
                                             is_active=True)
            password = secrets.token_urlsafe(6)
            user.set_password(password)
            send_password(user.email, password)
            user.save()
        except IntegrityError:
            user = get_object_or_404(CustomUser, email=data.get("email"))

        token, created = Token.objects.get_or_create(user=user)

        return Response(data={"auth_token": token.key}, status=200)


class YandexOauthView(generics.GenericAPIView):
    serializer_class = YandexOAuthSerializer

    def post(self, request, *args, **kwargs):
        serializing = self.serializer_class(data=request.data)
        serializing.is_valid(raise_exception=True)
        validated_data = serializing.validated_data

        response = requests.get(f'{os.getenv("YANDEX_OAUTH")}?oauth_token={validated_data["access_token"]}')
        data = response.json()
        try:
            phone = data.get("default_phone", {"number": ""})
            user = CustomUser.objects.create(email=data.get("default_email"),
                                             first_name=data.get("first_name", ""),
                                             last_name=data.get("last_name", ""),
                                             phone_number=phone.get("number"),
                                             is_active=True)
            password = secrets.token_urlsafe(6)
            user.set_password(password)
            send_password(user.email, password)
            user.save()
        except IntegrityError:
            user = get_object_or_404(CustomUser, email=data.get("default_email"))

        token, created = Token.objects.get_or_create(user=user)

        return Response(data={"auth_token": token.key}, status=200)


class ActivateUser(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        post_url = os.getenv("BACKEND_URL") + "auth/users/activation/"
        post_data = {"uid": kwargs["uid"], "token": kwargs["token"]}
        result = requests.post(post_url, data=post_data)
        if result.status_code >= status.HTTP_300_MULTIPLE_CHOICES:
            html_content = render(request, '../templates/final.html', {'text': "Активация прошла неуспешно!"})
            return html_content

        html_content = render(request, '../templates/final.html', {'text': "Активация прошла Успешно!"})
        return html_content


class SendCodeNumberView(BaseAuthenticatedMixin, generics.GenericAPIView):
    serializer_class = SendCodePhoneSerializer

    def post(self, request, *args, **kwargs):
        serialized_data = self.serializer_class(data=request.data)
        serialized_data.is_valid(raise_exception=True)
        validated_data = serialized_data.validated_data

        if request.user.is_phone_valid:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"msg": "phone is already validated"})

        payload_dicted = {
            "number": validated_data["number"],
            "code": ''.join(random.choices(string.digits, k=4))
        }
        payload = json.dumps(payload_dicted)
        headers = {
            'Authorization': os.getenv("MOBILEGROUP_KEY"),
            'Content-Type': 'application/json'
        }

        response = requests.post(url=os.getenv("MOBILEGROUP_URL"), data=payload, headers=headers)
        response_data = response.json()
        if response_data["result"] == "ok":
            cache.set(response_data["number"], response_data["code"], 900)
        return Response(status=response.status_code, data=response.json())


class ValidateCodeNumberView(BaseAuthenticatedMixin, generics.GenericAPIView):
    serializer_class = ValidateCodePhoneSerializer

    def post(self, request, *args, **kwargs):
        serialized_data = self.serializer_class(data=request.data)
        serialized_data.is_valid(raise_exception=True)
        validated_data = serialized_data.validated_data
        if cache.get(validated_data["number"]) == validated_data["code"]:
            request.user.is_phone_valid = True
            request.user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)









