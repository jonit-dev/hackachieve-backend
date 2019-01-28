from django.db import models

# Create your models here.
from apps.boards.models import Board
from apps.users.models import User


class Column(models.Model):
    name = models.CharField(max_length=255)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):  # title on dashboard
        return self.name
