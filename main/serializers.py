from rest_framework import serializers

from main.models import *


class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = '__all__'


class NewsLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsLetter
        fields = '__all__'


class MonthOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthOffers
        fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'


class LimitOffsetSerializer(serializers.Serializer):
    limit = serializers.IntegerField(default=5)
    offset = serializers.IntegerField(default=0)
