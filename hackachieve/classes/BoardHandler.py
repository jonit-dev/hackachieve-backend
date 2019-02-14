from datetime import datetime, timezone

from django.forms import model_to_dict

from apps.columns.models import Column
from apps.columns_categories.models import Column_category
from apps.goals.models import Goal
from apps.users_categories.models import User_Category


class BoardHandler:

    @staticmethod
    def diff_dates(date1, date2):
        return abs(date2 - date1).days

    @staticmethod
    def get_columns_and_goals(board, goal_type):

        # THIS FUNCTION IS RESPONSIBLE FOR FETCHING ALL BOARD RELATED DATA (columns, goals) AND CONSTRUCTING IT INTO A DICTIONARY (what will be sent over to the client as JSON)

        columns = Column.objects.filter(board_id=board.id)

        # convert queryset (django model) into list of objects. On this case, get only name and id attributes
        columns = list(columns.values())

        # loop trough all columns and search for goals and categories (that will be added in our answer)
        for column in columns:

            if goal_type == 'standby':
                goals = Goal.objects.filter(column_id=column['id'], status=1)
            elif goal_type == 'ongoing':
                goals = Goal.objects.filter(column_id=column['id'], status=2)
            elif goal_type == 'completed' or goal_type == 'done':
                goals = Goal.objects.filter(column_id=column['id'], status=3)  # done
            elif goal_type == 'all':
                goals = Goal.objects.filter(column_id=column['id'])
            else:
                goals = Goal.objects.filter(column_id=column['id'])

            total_completed_goals = len(goals.filter(status=False))  # status = False means the goal was accomplished

            categories = Column_category.objects.filter(column=column['id'])

            categories_data = []
            for category in categories:
                categories_data.append(
                    {'id': category.id, 'name': User_Category.objects.get(pk=category.id).category_name})

            # get this model using a filter
            goals = list(goals.values())
            column['goals'] = goals
            column['total_completed_goals'] = total_completed_goals
            column['total_goals'] = len(goals)
            column['categories'] = categories_data
            column['days_to_complete'] = BoardHandler.diff_dates(datetime.now(timezone.utc), column['deadline'])

        response = {
            'board': model_to_dict(board),
        }
        response['board']['columns'] = columns
        return response
