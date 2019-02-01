from django.db import models

# Create your models here.
from apps.columns.models import Column
from apps.goals.models import Goal


class Column_goal(models.Model):
    column = models.ManyToManyField(Column)
    goal = models.ManyToManyField(Goal)

    @classmethod
    def attach(cls, column, goal):
        # first create empty record on database
        column_goal = Column_goal()
        column_goal.save()

        column_goal.column.add(column)
        column_goal.goal.add(goal)
