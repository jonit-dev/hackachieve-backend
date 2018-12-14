from rentalmoose.classes.API import API


class UserHandler:

    @staticmethod
    def capitalize_name(name):

        adjusted_name = name.lower()
        adjusted_name = adjusted_name[:1].upper() + adjusted_name[1:]

        return adjusted_name

    @staticmethod
    def is_landlord(user):
        if user.type != 2:
            return False
        else:
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