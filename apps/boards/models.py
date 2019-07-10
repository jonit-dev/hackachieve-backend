from django.db import models
from apps.projects.models import Project
from apps.users.models import User


class Board(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, default=None)
    project = models.ForeignKey(Project,  on_delete=models.CASCADE, null=True)

    def __str__(self):  # title on dashboard
        return self.name

    @staticmethod
    def check_board_exists(board_id):
        return Board.objects.filter(pk=board_id).exists()

    @staticmethod
    def check_user_has_board(user_id, board_name):
        return Board.objects.filter(name=board_name, user_id=user_id).exists()
