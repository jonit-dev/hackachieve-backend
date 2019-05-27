from django.db import models

class Area_of_knowledge(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):  # title on dashboard
        return self.name
