from django.db import models

from apps.property_types.models import Property_type
from apps.resumes.models import Resume


# Create your models here.


class User_property_filter(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, default=None)
    max_budget = models.FloatField()
    moving_date = models.DateField(null=True)
    rent_anywhere = models.BooleanField(default=True)
    pet_friendly = models.BooleanField(default=False)

    def __str__(self):  # title on dashboard
        return self.resume
