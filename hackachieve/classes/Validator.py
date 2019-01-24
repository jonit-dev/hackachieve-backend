import re

from apps.users.models import User


class Validator:

    @staticmethod
    def check_resume_fields(resume_fields):

        required_fields = [
            'description',
            'tenancyLength',
            'totalHouseholdMembers',
            'consentCriminalCheck',
            'consentCreditCheck',
            'evictionHistory',
            'currentPropertyInfestations',
            'hasPet',
            'working',
            'maximumRentalBudget',
            'totalHouseholdIncome',
            'neighborhoodsOfInterest',
            'citiesOfInterest',
            'propertyTypes',
            'rentAnywhere',
            'propertyRequirements',
            'hasMoveInDate',
        ]

        conditional_fields = {
            "occupation": "working",
            "monthlyWage": "working",
            "moveInDate": "hasMoveInDate",
        }

        empty_fields = []

        for field in resume_fields:
            if field in required_fields:
                if resume_fields[field] is None or resume_fields[field] == "":
                    empty_fields.append(field)
            if field in conditional_fields:
                if resume_fields[conditional_fields[field]] is None or resume_fields[conditional_fields[field]] == "":
                    empty_fields.append(field)

        if len(empty_fields) > 0:
            return Validator.create_empty_fields_list(empty_fields)
        else:
            return True

    def split_upper(s):
        return filter(None, re.split("([A-Z][^A-Z]*)", s))

    @staticmethod
    def are_request_fields_valid(user_fields):


        empty_fields = []
        pretty_fields = []  # store the final results, that we'll make pretty for user output

        for key in user_fields:


            if key.startswith("optional_") == False:  # if its not an optional field...

                if user_fields[key] == "" or user_fields[key] == None:
                    empty_fields.append(key)

        if len(empty_fields) > 0:
            # error in results
            return Validator.create_empty_fields_list(empty_fields)
        else:
            return True

    @staticmethod
    def create_empty_fields_list(empty_fields):
        pretty_fields = []
        for e in empty_fields:
            e = Validator.split_upper(e)

            pretty_fields.append(" ".join(list(e)).capitalize().replace("_", " "))
            print(list(e))

        return ", ".join(pretty_fields)

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
