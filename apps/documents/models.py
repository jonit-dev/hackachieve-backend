from django.db import models

# Create your models here.
from apps.users.models import User


def validate_file_extension(value):
    import os
    megabyte_limit = 15
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]
    invalid_extensions = ['.exe']
    if ext.lower() in invalid_extensions:
        raise ValidationError(u'Unsupported file extension.')
    if value.size > megabyte_limit * 1024 * 1024:
        raise ValidationError("Max file size is %sMB" % str(megabyte_limit))


class MediaFile(models.Model):
    file = models.FileField(upload_to='static/file', blank=False, max_length=255, validators=[validate_file_extension])
    title = models.CharField(blank=True, null=True, max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


