from django.db import models


class Car(models.Model):
    name = models.CharField(max_length=50, blank=False)
    number = models.CharField(max_length=4, blank=False)
