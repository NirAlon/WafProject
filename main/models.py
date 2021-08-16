from django.db import models

class Logger(models.Model):
    email = models.CharField(max_length=255)
    date = models.DateTimeField()
    threshold = models.IntegerField(blank=True, null=True)
    type_attack = models.CharField(max_length=255)
    command = models.CharField(max_length=1024)
    if_warn = models.BooleanField()

class UsersDemo(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)


class FlagWaf:
    flag_waf = models.BooleanField()
    @property
    def lag_waf(self):
        print(self.flag_waf, "Waf flag is: ")
        return self.flag_waf


class User_value:
    user = None
    @property
    def user_val(self):
        print("user is:", self.user)
        return self.user


class WafTreshold:
    threshold_xss = models.FloatField()
    threshold_sql = models.FloatField()

    @property
    def threshold_xss(self):
        return self.threshold_xss
    @property
    def threshold_sql(self):
        return self.threshold_sql