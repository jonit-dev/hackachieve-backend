from django.db import models

# Create your models here.
from apps.goals.models import Goal
from apps.users_categories.models import User_Category


class Goal_category(models.Model):
    goal = models.ManyToManyField(Goal)
    category = models.ManyToManyField(User_Category)



    @classmethod
    def attach(cls, goal, category):
        # first create empty record on database
        goal_category = Goal_category()
        goal_category.save()

        goal_category.category.add(category)
        goal_category.goal.add(goal)
