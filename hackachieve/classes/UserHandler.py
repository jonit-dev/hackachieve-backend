import datetime
from apps.boards.models import Board
from apps.columns.models import Column
from apps.columns_categories.models import Column_category
from apps.goals.models import Goal
from apps.users_categories.models import User_Category
from hackachieve.classes.API import API


class UserHandler:

    @staticmethod
    def capitalize_name(name):

        adjusted_name = name.lower()
        adjusted_name = adjusted_name[:1].upper() + adjusted_name[1:]

        return adjusted_name

    @staticmethod
    def generate_initial_boards_columns(user):

        # This script is responsible for generating board default columns, goals and categories after user registering

        # BOARDS =========================== #

        long_term_board = Board(
            name="Long Term Goals",
            type=1,
            user_id=user.id
        )
        long_term_board.save()

        short_term_board = Board(
            name="Short Term Goals",
            type=2,
            user_id=user.id
        )
        short_term_board.save()

        # CATEGORIES =========================== #

        health = User_Category(
            category_name='Health',
            user_id=user.id
        )
        health.save()

        professional = User_Category(
            category_name='Professional',
            user_id=user.id
        )
        professional.save()

        financial = User_Category(
            category_name='Financial',
            user_id=user.id
        )
        financial.save()

        leisure = User_Category(
            category_name='Leisure',
            user_id=user.id
        )
        leisure.save()

        # COLUMNS =========================== #

        now = datetime.datetime.now()

        column_sprint = Column(
            name="Lose 1kg in 10 days",
            user_id=user.id,
            board_id=short_term_board.id,
            deadline=now + datetime.timedelta(days=10)  # set a default 10 days deadline for this sample column
        )
        column_sprint.save()

        Column_category.attach(column_sprint, health)  # set a sample category for this one

        # todo: set column category

        # GOALS =========================== #
        # sample goals


        goal = Goal(
            title="This is a sample goal",
            description="Description here",
            duration_hrs=None,
            deadline=now + datetime.timedelta(days=3),
            priority=0,
            column_id=column_sprint.id,
            user_id=user.id,
            status=1)  # active
        goal.save()


    @staticmethod
    def shorten_name(name):
        name_data = name.split(" ")

        first_name = name_data[0]

        last_name = []
        i = 0
        for data in name_data:
            if i is not 0:
                last_name.append(data[0].upper() + ".")

            i = i + 1

        output = "{} {}".format(first_name, " ".join(last_name))

        return output
