from django.contrib import admin

# Register your models here.
from apps.goals.models import Goal

admin.site.register(Goal)
