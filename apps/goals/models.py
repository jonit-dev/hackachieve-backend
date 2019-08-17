from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
from apps.columns.models import Column
from apps.documents.models import MediaFile
from apps.labels.models import Label
from apps.users.models import User


class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration_hrs = models.IntegerField(default=None, blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    column = models.ForeignKey(Column, on_delete=models.CASCADE)
    priority = models.IntegerField(default=0, blank=True)
    status = models.IntegerField(default=1)  # 1 = standby, 2 = ongoing, 3=done
    order_position = models.IntegerField(default=0, blank=True)
    labels = models.ManyToManyField(Label, default=None)
    is_public = models.BooleanField(default=False)
    member = models.ManyToManyField(User, related_name="goal_member")
    file = models.ForeignKey(MediaFile, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):  # title on dashboard
        return self.title

    @staticmethod
    def check_user_owns_goal(user_id, goal_id):
        goal = Goal.objects.get(pk=goal_id)

        if goal.user.id is user_id:
            return True
        else:
            return False

    @staticmethod
    def check_goal_by_id(user_id, goal_id):
        return Goal.objects.filter(user_id=user_id, id=goal_id).exists()

    @staticmethod
    def check_goal_by_title(user_id, goal_title):
        return Goal.objects.filter(user_id=user_id, title=goal_title).exists()


class GoalComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class CommentVote(models.Model):

    VOTE_CHOICES = [
        (0, 0),
        (1, 1),
    ]
    comment = models.ForeignKey(
        GoalComment, on_delete=models.CASCADE, related_name='commentvote')
    upvote = models.IntegerField(default=0, choices=VOTE_CHOICES)
    downvote = models.IntegerField(default=0, choices=VOTE_CHOICES)


# method for updating order_position with fo
@receiver(post_save, sender=Goal)
def update_order(sender, instance, **kwargs):
    if instance.order_position is None:
        instance.order_position = instance.id
        instance.save()
