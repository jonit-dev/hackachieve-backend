from django.db import models

# Create your models here.


class Label(models.Model):
    name = models.CharField(max_length=255)


    def __str__(self):  # title on dashboard
        return self.name
