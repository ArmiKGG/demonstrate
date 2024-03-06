import os

from django.contrib.auth import get_user_model

User = get_user_model()
from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(email=os.getenv("DJANGO_SUPERUSER_EMAIL")).exists():
            user = User.objects.create_superuser(password=os.getenv("DJANGO_SUPERUSER_PASSWORD"),
                                                 email=os.getenv("DJANGO_SUPERUSER_EMAIL"),
                                                 first_name="admin",
                                                 last_name="admin",
                                                 phone_number="+9112345678")

            Token.objects.create(user=user)
            print('Admin created')
        else:
            print('Admin is already exists')
