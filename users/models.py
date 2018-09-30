# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # add additional fields in here

    # type 1 = tenant, type 2 = landlord, type 3 = real estate agency
    type = models.IntegerField(default=1)
    email = models.CharField(max_length=255)

    def __str__(self):
        return self.email



