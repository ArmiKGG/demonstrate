from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Direction(models.Model):
    icon = models.ImageField(blank=True, null=True)
    name = models.CharField(max_length=256, unique=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id) + ": " + self.name


class NewsLetter(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return str(self.email)


class MonthOffers(models.Model):
    icon = models.ImageField(blank=True, null=True)
    name = models.CharField(max_length=256, unique=True)
    address = models.CharField(max_length=512, blank=True, null=True)
    description = models.TextField(max_length=1028, blank=True, null=True)
    views = models.IntegerField(default=0)
    rating = models.IntegerField(default=1,
                                 validators=[
                                     MaxValueValidator(5),
                                     MinValueValidator(1)
                                 ])

    def __str__(self):
        return str(self.id) + ": " + self.name


class News(models.Model):
    icon = models.ImageField(blank=True, null=True)
    name = models.CharField(max_length=256, unique=True)
    views = models.IntegerField(default=0)
    description = models.TextField(max_length=2056, blank=True, null=True)
    date = models.DateField(default=datetime.now)

    def __str__(self):
        return str(self.id) + ": " + self.name
