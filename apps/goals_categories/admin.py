from django.contrib import admin

# Register your models here.
from apps.goals_categories.models import Goal_category

admin.site.register(Goal_category)
