from django.contrib import admin

# Register your models here.
from apps.users_goals_categories.models import User_Goal_Category

admin.site.register(User_Goal_Category)
