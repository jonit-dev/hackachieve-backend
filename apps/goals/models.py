from django.db import models

# Create your models here.
from apps.columns.models import Column
from apps.users.models import User


class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    duration_hrs = models.IntegerField(default=None, null=True)
    deadline = models.DateTimeField(auto_now_add=True)
    column = models.ForeignKey(Column, on_delete=models.CASCADE)
    priority = models.BooleanField(default=0)
    status = models.IntegerField(default=1)  # 1 = standby, 2 = ongoing, 3=done

    def __str__(self):  # title on dashboard
        return self.title

    @staticmethod
    def check_goal_by_id(user_id, goal_id):
        return Goal.objects.filter(user_id=user_id, id=goal_id).exists()

    @staticmethod
    def check_goal_by_title(user_id, goal_title):
        return Goal.objects.filter(user_id=user_id, title=goal_title).exists()

