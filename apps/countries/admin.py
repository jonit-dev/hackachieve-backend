from django.contrib import admin

# Register your models here.
from apps.countries.models import Country

admin.site.register(Country)