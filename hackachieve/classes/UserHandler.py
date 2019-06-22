import datetime

from apps.area_of_knowledges.models import Area_of_knowledge
from apps.boards.models import Board
from apps.columns.models import Column
from apps.goals.models import Goal
from apps.labels.models import Label
from hackachieve.classes.API import API


class UserHandler:

    @staticmethod
    def capitalize_name(name):

        adjusted_name = name.lower()
        adjusted_name = adjusted_name[:1].upper() + adjusted_name[1:]

        return adjusted_name

    @staticmethod
    def attach_area_of_knowledge(user, aoks):

        # loop through each AOK (area of knowledge)
        for aok in aoks:

            aok_check = Area_of_knowledge.objects.filter(name__exact=aok['name'])

            # if exists, attach to request user
            if aok_check.exists():

                # print('AOK already exists. Attaching to user...')

                user.areas_of_knowledge.add(aok_check.first())
                user.save()

            else:

                # if not, create a new one
                # print('Creating and attaching AOK to user')

                aok = Area_of_knowledge(
                    user=user,
                    name=aok['name']
                )
                aok.save()

                # and attach to user

                user.areas_of_knowledge.add(aok)
                user.save()

    @staticmethod
    def generate_initial_boards_columns(user):

        # This script is responsible for generating board default columns, goals and categories after user registering

        # BOARDS =========================== #

        board = Board(
            name="Family",
            user_id=user.id,
            description="Everything"
        )
        board.save()

        health_board = Board(
            name="Health",
            user_id=user.id,
            description="Goals to get in shape until the summer"
        )
        health_board.save()

        board = Board(
            name="Career",
            user_id=user.id,
            description="Things to learn to leverage my career"
        )
        board.save()

        board = Board(
            name="Finances",
            user_id=user.id,
            description="Achieve financial freedom"
        )
        board.save()

        board = Board(
            name="Personal Development",
            user_id=user.id,
            description="Improve myself"
        )
        board.save()

        board = Board(
            name="Spiritual",
            user_id=user.id,
            description="Become a meditation master"
        )
        board.save()

        board = Board(
            name="Leisure and Fun",
            user_id=user.id,
            description="Everybody needs to relax"
        )
        board.save()

        # LABELS =========================== #

        # creating default ones

        high_priority_label = Label(name='High Priority', user=user).save()
        medium_priority_label = Label(name='Medium Priority', user=user).save()
        low_priority_label = Label(name='Low Priority', user=user).save()

        # COLUMNS =========================== #

        now = datetime.datetime.now()

        column_sprint = Column(
            name="Lose 10kg in 20 days",
            user_id=user.id,
            board_id=health_board.id,
            deadline=now + datetime.timedelta(days=20),  # set a default 20 days deadline for this sample column
            description='Get in shape'
        )
        column_sprint.save()

        # GOALS =========================== #
        # sample goals

        goal = Goal(
            title="Subscribe to a gym plan",
            description="This is just a short term goal sample",
            duration_hrs=None,
            deadline=now + datetime.timedelta(days=3),
            column_id=column_sprint.id,
            user_id=user.id)  # active
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
