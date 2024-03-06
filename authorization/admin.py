# Register your models here.
from django.contrib import admin

from authorization.models import CustomUser

admin.site.register(CustomUser)
