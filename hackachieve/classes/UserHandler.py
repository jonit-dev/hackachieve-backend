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

            aok_check = Area_of_knowledge.objects.filter(
                name__exact=aok['name'])

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

    # @staticmethod
    # def generate_initial_boards_columns(user):

        # This script is responsible for generating board default columns, goals and categories after user registering

        # BOARDS =========================== #

        # LABELS =========================== #

        # creating default ones

        # COLUMNS =========================== #

        # GOALS =========================== #
        # sample goals

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
