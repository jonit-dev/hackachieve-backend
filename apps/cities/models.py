from django.db import models

# Create your models here.
from apps.provinces.models import Province


class City(models.Model):
    name = models.CharField(max_length=255)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)



    def __str__(self):  # title on dashboard
        return self.name
