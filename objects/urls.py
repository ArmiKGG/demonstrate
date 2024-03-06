from django.urls import path

from objects import views

app_name = "objects"

urlpatterns = [
    path('', views.RestObjectView.as_view(), name="rest_obj"),
    path('types/', views.TypeInfoView.as_view(), name="type_obj"),
    path('directions_info/', views.DirectionsInfoListView.as_view(), name="directions_list_create"),
    path('directions_info/<int:pk>/', views.DirectionsInfoCRUDView.as_view(), name="directions_crud"),
]
