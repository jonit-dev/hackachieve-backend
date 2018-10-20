from django.contrib import admin

# Register your models here.
from apps.properties.models import Property

admin.site.register(Property)
