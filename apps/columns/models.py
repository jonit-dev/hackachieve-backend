from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
from apps.boards.models import Board
from apps.users.models import User
from hackachieve.classes.API import API


class Column(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, default=None)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deadline = models.DateTimeField(null=True, default=None)
    order_position = models.IntegerField(null=True, blank=True)
    member = models.ManyToManyField(User, related_name="column_member")

    def __str__(self):  # title on dashboard
        return self.name

    @staticmethod
    def check_exists(column_id):
        return Column.objects.filter(id=column_id).exists()


# method for updating order_position with fo
@receiver(post_save, sender=Column)
def update_order(sender, instance, **kwargs):
    if instance.order_position is None:
        instance.order_position = instance.id
        instance.save()
