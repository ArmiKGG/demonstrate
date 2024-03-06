from rest_framework import serializers

from objects.models import *


class TypeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeInfo
        fields = '__all__'


class RestObjectSerializer(serializers.ModelSerializer):
    types_info = TypeInfoSerializer(many=True)

    class Meta:
        model = RestObject
        fields = '__all__'


class RestObjectSerializerCreate(serializers.ModelSerializer):
    types_info = serializers.ListField(child=serializers.JSONField())

    class Meta:
        model = RestObject
        fields = '__all__'


class DirectionsInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectionsInfo
        fields = '__all__'
