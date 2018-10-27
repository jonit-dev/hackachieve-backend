# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # add additional fields in here

    # type 1 = tenant, type 2 = landlord, type 3 = real estate agency
    type = models.IntegerField(default=1)
    email = models.CharField(max_length=255, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_resume(self):

        if len(self.resume_set.all()) > 0:
            return True
        else:
            return False


