from django.db import models
from apps.goals.models import Goal
from apps.users.models import User


class Checklist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    description = models.TextField(default=None)
    status = models.BooleanField(default=0)

    def __str__(self):  # title on dashboard
        return self.description
