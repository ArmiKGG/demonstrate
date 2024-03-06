from django.db import models


class RestObject(models.Model):
    types_info = models.ManyToManyField(to="objects.TypeInfo", blank=True)
    object_name = models.JSONField(null=True, blank=True)
    main_info = models.JSONField(null=True, blank=True)
    payment_info = models.JSONField(null=True, blank=True)


class TypeInfo(models.Model):
    info = models.JSONField(null=True, blank=True)


class DirectionsInfo(models.Model):
    class SeasonsChoices(models.TextChoices):
        Summer = "Лето", "Лето"
        Winter = "Зима", "Зима"
        All_season = "Круглый Год", "Круглый Год"

    directions = models.JSONField(null=True, blank=True)
    season = models.CharField(choices=SeasonsChoices.choices, null=True, blank=True)
    services = models.JSONField(null=True, blank=True)
