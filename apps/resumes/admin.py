from django.contrib import admin

# Register your models here.
from apps.resumes.models import Resume

admin.site.register(Resume)