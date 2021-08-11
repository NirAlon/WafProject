from django.db import models


class Hero(models.Model):
    name = models.CharField(max_length=60)
    alias = models.CharField(max_length=60)
    def __str__(self):
        return self.name

class Waf(models.Model):
    sql_injection = models.CharField(max_length=60)
    xss_attack = models.CharField(max_length=60)
    def __str__(self):
        return self.sql_injection, self.xss_attack