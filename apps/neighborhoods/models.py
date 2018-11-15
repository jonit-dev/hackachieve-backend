from django.db import models

# Create your models here.
from apps.cities.models import City


class Neighborhood(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE, default=None)
    description = models.TextField(default=None)

    def __str__(self):  # title on dashboard
        return self.name
