import email
from statistics import mode
from django.conf import settings
from django.db import models


class Account(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=30)
