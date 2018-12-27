from django.db import models
from apps.neighborhoods.models import Neighborhood
from apps.resumes.models import Resume

class Resume_neighborhood(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE)
