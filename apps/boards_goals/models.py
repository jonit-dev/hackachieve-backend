from django.db import models

# Create your models here.
from apps.boards.models import Board
from apps.goals.models import Goal


class Board_goal(models.Model):
    board = models.ManyToManyField(Board)
    goal = models.ManyToManyField(Goal)



    @classmethod
    def attach(cls, board, goal):
        board_goal = Board_goal()
        board_goal.save()

        board_goal.board.add(board)
        board_goal.goal.add(goal)
