
from django.db import models


class Logger(models.Model):
    email = models.CharField(max_length=255)
    date = models.DateTimeField()
    threshold = models.IntegerField(blank=True, null=True)
    type_attack = models.CharField(max_length=255)
    command = models.CharField(max_length=1024)
    if_warn = models.BooleanField()


class UserDemo(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
