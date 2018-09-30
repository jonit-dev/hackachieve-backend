from django.contrib import admin

# Register your models here.
from apps.provinces.models import Province

admin.site.register(Province)