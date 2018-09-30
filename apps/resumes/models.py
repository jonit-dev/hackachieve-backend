from django.db import models

# Create your models here.
from apps.users.models import User


class Resume(models.Model):
    tenant = models.ForeignKey(User, on_delete=models.CASCADE)

    #location
    # city = models.ForeignKey(City, on_delete=models.CASCADE)
    phone = models.CharField(max_length=255)
    description = models.TextField()
    zipcode = models.CharField(max_length=255)
    address = models.TextField()

    #property damage risk
    expected_tenancy_length = models.IntegerField(default=1)
    total_household_members = models.IntegerField(default=1)
    consent_criminal_check = models.BooleanField()
    eviction_history = models.BooleanField()
    current_property_has_bedbugs = models.BooleanField()
    has_pet = models.BooleanField()

    #financial risk
    currently_working = models.BooleanField()
    current_ocupation = models.CharField(max_length=255)
    credit_score = models.IntegerField()
    maximum_rental_budget = models.FloatField()
    current_wage = models.FloatField()

    def __str__(self):  # title on dashboard
        return self.tenant.username
