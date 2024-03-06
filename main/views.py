from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from main.serializers import *


class DirectionListView(generics.ListAPIView):
    serializer_class = DirectionSerializer
    queryset = Direction.objects.all()


class NewsLetterListView(generics.ListCreateAPIView):
    serializer_class = NewsLetterSerializer
    queryset = NewsLetter.objects.all()


class MonthOffersListView(generics.ListAPIView):
    serializer_class = MonthOfferSerializer
    queryset = MonthOffers.objects.all()


class NewsListView(generics.ListAPIView):
    serializer_class = NewsSerializer
    queryset = News.objects.all()


class TopDirectionListView(generics.GenericAPIView):
    serializer_class = DirectionSerializer
    request_serializer_class = LimitOffsetSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'limit',
                openapi.IN_QUERY,
                description="pagination limit (default value is 5)",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                'offset',
                openapi.IN_QUERY,
                description="pagination offset (default value is 0)",
                type=openapi.TYPE_INTEGER,
            )
        ],
    )
    def get(self, request, *args, **kwargs):
        validated_data = self.request_serializer_class(data=self.request.GET)
        validated_data.is_valid(raise_exception=True)
        serialized_data = validated_data.validated_data

        top_directions = Direction.objects.all().order_by("-views")[
                         serialized_data["offset"]:
                         serialized_data["offset"] + serialized_data["limit"]
                         ]

        return Response(data=self.serializer_class(instance=top_directions, many=True).data,
                        status=status.HTTP_200_OK)
