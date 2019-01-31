from django.db import models

# Create your models here.
from apps.boards.models import Board
from apps.users.models import User
from hackachieve.classes.API import API


class Column(models.Model):
    name = models.CharField(max_length=255)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):  # title on dashboard
        return self.name

    @staticmethod
    def check_exists(column_id):
        check_column = Column.objects.filter(id=column_id)
        if len(check_column) is 0:
            return False
        else:
            return True
