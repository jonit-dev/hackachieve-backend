from django.db import models

# Create your models here.
from apps.property_types.models import Property_type
from apps.user_property_filter.models import User_property_filter


class User_property_filter_property_type(models.Model):
    property_filter = models.ForeignKey(User_property_filter, on_delete=models.CASCADE)
    property_type = models.ForeignKey(Property_type,on_delete=models.CASCADE)

    def __str__(self):  # title on dashboard
        return self.property_filter

