from django.contrib import admin

# Register your models here.
from apps.checklists.models import Checklist

admin.site.register(Checklist)
