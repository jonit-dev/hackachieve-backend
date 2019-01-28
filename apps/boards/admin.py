from django.contrib import admin

# Register your models here.
from apps.boards.models import Board

admin.site.register(Board)
