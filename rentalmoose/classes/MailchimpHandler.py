from apps.users.models import User
from rentalmoose.classes.Environment import *
from mailchimp3 import MailChimp

mailchimp_api_key = Environment.getkey('mailchimp_api_key')

lists = {
    "Tenants":
        {
            "Vancouver": "67c4078a52",
            "TestList": "bfeeacc775"
        },
    "Landlords":
        {
            "Vancouver": "3bd184ac87"
        }
}


class MailchimpHandler:

    @staticmethod
    def addLead(email, listType, listName, tags):
        client = MailChimp(mc_api=mailchimp_api_key, mc_user='rentalmoose', timeout=10.0)

        # add lead to list

        client.lists.members.create(lists[listType][listName], {
            'email_address': email,
            'status': 'subscribed',
            'merge_fields': tags,
        })

        # add city of interest

        # user = User.objects.get(email=email)
        #
        # cities_of_interest = user.resume_set.all().first().resume_city_set.all()
        #
        # for city in cities_of_interest:
        #
        #     client.lists.interest_categories.interests.create(list_id=lists[listType][listName], category_id='', data={})



        return True
