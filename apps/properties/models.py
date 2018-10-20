from django.db import models

# Create your models here.
from apps.property_types.models import Property_type
from apps.users.models import User

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models

property_root = FileSystemStorage(location=settings.PROPERTIES_IMAGES_ROOT)

class Property(models.Model):
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE)
    upload = models.FileField(storage=property_root,default=False)
    status = models.BooleanField(default=1)
    title = models.CharField(max_length=255)
    sqft = models.IntegerField()
    type_id = models.ForeignKey(Property_type, on_delete=models.CASCADE, default=2)
    rental_value = models.FloatField()
    utilities_included = models.BooleanField()
    n_bedrooms = models.IntegerField()
    n_bathrooms = models.IntegerField()
    address = models.CharField(max_length=255)
    furnished = models.BooleanField()
    no_pets = models.BooleanField()
    no_smoking = models.BooleanField()
    no_parties = models.BooleanField()
    minimum_lease = models.IntegerField()
    pet_deposit = models.FloatField()
    security_deposit = models.FloatField()
    publication_date = models.DateTimeField()
    available_to_move_in_date = models.DateField()
    open_view_start = models.DateTimeField()
    open_view_end = models.DateTimeField()

    def __str__(self):  # title on dashboard
        return self.title

