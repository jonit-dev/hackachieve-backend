from django.contrib import admin

# Register your models here.
from countries.models import Country

admin.site.register(Country)