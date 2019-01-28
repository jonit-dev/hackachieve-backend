from apps.boards.models import Board
from apps.columns.models import Column
from hackachieve.classes.API import API


class UserHandler:

    @staticmethod
    def capitalize_name(name):

        adjusted_name = name.lower()
        adjusted_name = adjusted_name[:1].upper() + adjusted_name[1:]

        return adjusted_name

    @staticmethod
    def generate_initial_boards_columns(user):

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

        # COLUMNS =========================== #

        boards = Board.objects.filter(user_id=user.id)

        for b in boards:
            column_sprint = Column(
                name="Weekly Sprint",
                user_id=user.id,
                board_id=b.id
            )
            column_sprint.save()

            column_on_going = Column(
                name="On Going",
                user_id=user.id,
                board_id=b.id
            )
            column_on_going.save()

            column_done = Column(
                name="Done",
                user_id=user.id,
                board_id=b.id
            )
            column_done.save()

        return True

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