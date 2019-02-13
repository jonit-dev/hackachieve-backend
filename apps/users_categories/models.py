from django.db import models

# Create your models here.
from apps.users.models import User


class User_Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=255)

    def __str__(self):  # title on dashboard
        return self.category_name

    @staticmethod
    def check_category_exists(category_name, user_id):
        return User_Category.objects.filter(category_name=category_name, user_id=user_id).exists()
