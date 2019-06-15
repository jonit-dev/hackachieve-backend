from django.db import models

# Create your models here.
from apps.users.models import User


class Label(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)


    def __str__(self):  # title on dashboard
        return self.name
