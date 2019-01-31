from django.db import models

# Create your models here.
from apps.columns.models import Column
from apps.users.models import User
from hackachieve.classes.API import API


class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    duration_hrs = models.IntegerField(default=None, null=True)
    deadline = models.DateTimeField(auto_now_add=True)
    column = models.ForeignKey(Column, on_delete=models.CASCADE)
    column_day = models.IntegerField(default=0)
    priority = models.BooleanField(default=0)

    def __str__(self):  # title on dashboard
        return self.title

    @staticmethod
    def check_goal(user_id, goal_title):
        check_goal = Goal.objects.filter(user_id=user_id, title=goal_title)

        if len(check_goal) >= 1:
            return True
        else:
            return False
