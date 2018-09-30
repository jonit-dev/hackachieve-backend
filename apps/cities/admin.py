from django.contrib import admin

# Register your models here.
from apps.cities.models import City

admin.site.register(City)