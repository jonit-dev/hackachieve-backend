from django.db import models

# Create your models here.
from apps.users.models import User


class Board(models.Model):
    name = models.CharField(max_length=255)
    type = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):  # title on dashboard
        return self.name

    @staticmethod
    def check_board_exists(board_id):
        return Board.objects.filter(pk=board_id).exists()

    @staticmethod
    def check_user_has_board(user_id, board_name):
        return Board.objects.filter(name=board_name, user_id=user_id).exists()
