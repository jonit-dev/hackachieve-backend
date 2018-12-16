from django.db import models


# Create your models here.

class Country(models.Model):
    name = models.CharField(max_length=255, default=None)
    abbrev = models.CharField(max_length=255, default=None)

    def __str__(self):  # title on dashboard
        return self.name
