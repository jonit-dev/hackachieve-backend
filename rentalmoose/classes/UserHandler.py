from rentalmoose.classes.API import API


class UserHandler:

    @staticmethod
    def is_landlord(user):
        if user.type != 2:
            return False
        else:
            return True
