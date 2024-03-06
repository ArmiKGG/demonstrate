from django.urls import path

from main import views

app_name = "main"

urlpatterns = [
    path('directions/', views.DirectionListView.as_view(), name="directions"),
    path('top/directions/', views.TopDirectionListView.as_view(), name="to-directions"),
    path('emails/', views.NewsLetterListView.as_view(), name="emails"),
    path('offers/', views.MonthOffersListView.as_view(), name="offers"),
    path('news/', views.NewsListView.as_view(), name="news"),
]
