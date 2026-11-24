from django.db import models
from django.contrib.auth.models import User


# UserInfo - 1:1 to User #
class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address_1 = models.CharField(max_length=100)
    address_2 = models.CharField(max_length=20, null=True, blank=True)
    zip_code = models.CharField(max_length=6)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)