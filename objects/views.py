from django.http import JsonResponse
from rest_framework import generics
from rest_framework import status

from authorization.mixins.auth import BaseAuthenticatedMixin
from objects.serializers import *
from utils.prettyjson import unpack


class TypeInfoView(BaseAuthenticatedMixin, generics.ListAPIView):
    serializer_class = TypeInfoSerializer

    def get(self, response, *args, **kwargs):
        objects = self.serializer_class(instance=TypeInfo.objects.all(), many=True).data
        return JsonResponse(data=unpack(objects), status=status.HTTP_200_OK, safe=False)


class RestObjectView(BaseAuthenticatedMixin, generics.ListCreateAPIView):
    serializer_class = RestObjectSerializer
    serializer_class_create = RestObjectSerializerCreate
    queryset = RestObject.objects.all()

    def create(self, request, *args, **kwargs):
        validated_data = self.serializer_class_create(data=self.request.data)
        validated_data.is_valid(raise_exception=True)
        type_infos = validated_data.validated_data["types_info"]

        obj = RestObject.objects.create(object_name=validated_data.validated_data["object_name"],
                                        main_info=validated_data.validated_data["main_info"],
                                        payment_info=validated_data.validated_data["payment_info"]
                                        )

        [obj.types_info.create(info=type_info) for type_info in type_infos]

        data = self.serializer_class(instance=obj).data

        return JsonResponse(data=data, status=status.HTTP_201_CREATED)


class DirectionsInfoListView(BaseAuthenticatedMixin, generics.ListCreateAPIView):
    serializer_class = DirectionsInfoSerializer
    queryset = DirectionsInfo.objects.all()
    http_method_names = ["get", "post"]


class DirectionsInfoCRUDView(BaseAuthenticatedMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DirectionsInfoSerializer
    queryset = DirectionsInfo.objects.all()
    http_method_names = ["get", "patch", "delete"]
