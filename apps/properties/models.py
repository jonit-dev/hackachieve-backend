from django.db import models

# Create your models here.
from apps.property_types.models import Property_type
from apps.users.models import User

from stdimage.models import StdImageField  # for image resizing
from django.conf import settings  # for saving image in particular folder
from django.core.files.storage import FileSystemStorage  # same as above
from django.db import models

property_root = FileSystemStorage(location=settings.PROPERTIES_IMAGES_ROOT)


def property_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{0}/{1}'.format(instance.owner.id, filename)


class Property(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # upload = models.FileField(storage=property_root,default=False)

    upload = StdImageField(upload_to=settings.PROPERTIES_IMAGES_ROOT, blank=True,
                           variations={
                               'large': (600, 400),
                               'thumbnail': (100, 100, True)
                           })
    status = models.BooleanField(default=1)
    title = models.CharField(max_length=255)
    sqft = models.IntegerField()
    type = models.ForeignKey(Property_type, on_delete=models.CASCADE, default=2)
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
