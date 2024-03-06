"""
URL configuration for TourCompass project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

from authorization.views import (ResetPasswordEmailView, ResetPasswordSendCodeView, GoogleOauthView, ActivateUser,
                                 YandexOauthView, SendCodeNumberView, ValidateCodeNumberView)

urlpatterns = [
    path('auth/activate/<str:uid>/<str:token>/', ActivateUser.as_view()),

    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

    path('auth/reset_email/send_code/', ResetPasswordSendCodeView.as_view()),
    path('auth/reset_email/validate/', ResetPasswordEmailView.as_view()),

    path('auth/o_auth/google/', GoogleOauthView.as_view()),
    path('auth/o_auth/yandex/', YandexOauthView.as_view()),

    path('auth/phone_validate/send_code/', SendCodeNumberView.as_view()),
    path('auth/phone_validate/validate/', ValidateCodeNumberView.as_view()),
]
