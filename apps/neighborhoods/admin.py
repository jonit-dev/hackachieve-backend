from django.contrib import admin

# Register your models here.
from apps.neighborhoods.models import Neighborhood

admin.site.register(Neighborhood)
