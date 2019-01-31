# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # add additional fields in here

    # type 1 = tenant, type 2 = landlord, type 3 = real estate agency
    email = models.CharField(max_length=255, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @staticmethod
    def check_user_exists(user_id):
        return User.objects.filter(pk=user_id).exists()
