from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.boards.models import Board
from apps.columns.models import Column
from apps.goals.models import Goal
from apps.projects.models import Project
from hackachieve.utils import START_UP_BOARD_LIST

GOAL_STATUS = {
    'standby': 1,
    'ongoing': 2,
    'completed': 3
}


# method for updating order_position with fo
@receiver(post_save, sender=Project)
def create_boards(sender, instance, **kwargs):
    if instance.id and instance.user and len(Board.objects.filter(project=instance)) == 0:
        for item in START_UP_BOARD_LIST:
            board = Board.objects.create(
                name=item['name'],
                description=item['description'],
                project_id=instance.id,
                user_id=instance.user.id
            )
            try:
                if item['long_term_goal'] and len(item['long_term_goal']) > 0:
                    for column in item['long_term_goal']:
                        column_obj = Column.objects.create(
                            name=column['name'],
                            board_id=board.id,
                            user_id=instance.user.id,
                            description=column['description'],
                            deadline=column['deadline'],
                            is_example=True
                        )
                        if column['short_term_goal'] and len(column['short_term_goal']) > 0:
                            for goal in column['short_term_goal']:
                                Goal.objects.create(
                                    title=goal['title'],
                                    column_id=column_obj.id,
                                    user_id=instance.user.id,
                                    description=goal['description'],
                                    deadline=goal['deadline']
                                )
            except KeyError:
                pass


