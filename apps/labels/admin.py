from django.contrib import admin

# Register your models here.
from apps.labels.models import Label

admin.site.register(Label)
