from django.db import models

# Create your models here.
from apps.cities.models import City
from apps.resumes.models import Resume

class Resume_city(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
