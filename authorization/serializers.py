from rest_framework import serializers

from authorization.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('password',)
        model = CustomUser


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    default_error_messages = {
        "cannot_create_user": "Unable to create account."
    }

    class Meta:
        model = CustomUser
        fields = ["email", "first_name", "last_name", "phone_number", "password"]

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=256, required=True)


class EmailCodeSerializer(EmailSerializer):
    code = serializers.CharField(max_length=10, required=True)


class GoogleOAuthSerializer(serializers.Serializer):
    access_token = serializers.CharField(max_length=2048, required=True)


class YandexOAuthSerializer(serializers.Serializer):
    access_token = serializers.CharField(max_length=2048, required=True)


class SendCodePhoneSerializer(serializers.Serializer):
    number = serializers.CharField(max_length=256, required=True)


class ValidateCodePhoneSerializer(SendCodePhoneSerializer):
    code = serializers.CharField(max_length=4)
