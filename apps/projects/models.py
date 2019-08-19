from django.db import models
from apps.users.models import User


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    member = models.ManyToManyField(User, related_name="member")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

