from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):
    email = models.EmailField()
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.username
