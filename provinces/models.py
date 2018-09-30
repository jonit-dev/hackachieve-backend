from django.db import models


# Create your models here.
from countries.models import Country


class Province(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    abbrev = models.CharField(max_length=255,default="")


    def __str__(self):  # title on dashboard
        return self.name
