from django.contrib import admin

# Register your models here.
from apps.users_categories.models import User_Category

admin.site.register(User_Category)
