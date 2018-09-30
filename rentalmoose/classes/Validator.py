import re

from apps.users.models import User


class Validator:

    def split_upper(s):
        return filter(None, re.split("([A-Z][^A-Z]*)", s))

    @staticmethod
    def are_user_fields_valid(user_fields):

        print(">> checking user fields")

        empty_fields = []
        pretty_fields = []  # store the final results, that we'll make pretty for user output

        for key in user_fields:
            if user_fields[key] == "":
                empty_fields.append(key)

        if len(empty_fields) > 0:
            # error in results

            for e in empty_fields:
                e = Validator.split_upper(e)
                pretty_fields.append(" ".join(list(e)).capitalize())
                print(list(e))

            return pretty_fields
        else:
            return True

    @staticmethod
    def check_password_confirmation(password, password_confirmation):

        if password == password_confirmation:
            return True
        else:
            return False

    @staticmethod
    def check_user_exists(email):

        if User.objects.filter(email=email).exists():
            return True
        else:
            return False

