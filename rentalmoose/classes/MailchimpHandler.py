import json
import requests
from rentalmoose.classes.Environment import *


class MailchimpHandler:
    print("Mailchimp API v3 handler")

    # ENV = Environment.getkey('env')
    # API_KEY = Environment.getkey('mailchimp_api_key')

    ENV = 'prod'
    API_KEY = "eb8ffce2d2623bb9570702a7aac3afa3-us19"


    API_URL = 'https://us19.api.mailchimp.com/3.0'
    USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'

    HEADERS = {
        'User-Agent': USER_AGENT,
        'Authorization': 'Basic {}'.format(API_KEY),
        'content-type': "application/json",
    }

    @staticmethod
    def add_subscriber(email, first_name, last_name, list_id="ec09a29d85"):

        if MailchimpHandler.ENV == 'dev':
            print('Mailchimp: skipping new subscriber register')

        else:

            print("Registering new subscriber: {}".format(email))
            url = '{}/lists/{}/members/'.format(MailchimpHandler.API_URL, list_id)

            values = {
                "email_address": email,
                "status": "subscribed",
                "merge_fields": {
                    "FIRSTNAME": first_name,
                    "LASTNAME": last_name
                }
            }
            response = requests.request("POST", url, data=json.dumps(values), headers=MailchimpHandler.HEADERS)

            return response.text

    @staticmethod
    def attach_tags(tags, subscriber, list_id="ec09a29d85"):

        if MailchimpHandler.ENV == 'dev':
            print('Mailchimp: skipping attaching tags to subscriber')

        else:

            print("Attaching tags ({}) to user {}".format(tags, subscriber))

            for tag in tags:
                tag_id = MailchimpHandler.get_tag_id(tag, list_id)

                if tag_id is not False:
                    MailchimpHandler.attach_tag(tag_id, subscriber, list_id)
                else:
                    new_tag_id = MailchimpHandler.create_new_tag(tag, list_id)
                    MailchimpHandler.attach_tag(new_tag_id, subscriber, list_id)

    @staticmethod
    def create_new_tag(tag_name, list_id="ec09a29d85"):

        print("Creating new tag ({}) for list {}".format(tag_name, list_id))

        url = '{}/lists/{}/segments/'.format(MailchimpHandler.API_URL, list_id)

        values = {
            "name": tag_name,
            "static_segment": []
        }

        response = requests.request("POST", url, data=json.dumps(values), headers=MailchimpHandler.HEADERS)

        json_data = json.loads(response.text)

        tag_id = json_data['id']

        return tag_id

        return

    @staticmethod
    def attach_tag(tag_id, subscriber, list_id="ec09a29d85"):

        print("Attaching tag {} to {} from list {}".format(tag_id, subscriber, list_id))

        url = '{}/lists/{}/segments/{}/members'.format(MailchimpHandler.API_URL, list_id, tag_id)

        values = {
            "email_address": subscriber
        }

        response = requests.request("POST", url, data=json.dumps(values), headers=MailchimpHandler.HEADERS)

        return response.text

    @staticmethod
    def get_tag_id(name, list_id="ec09a29d85"):

        url = '{}/lists/{}/segments'.format(MailchimpHandler.API_URL, list_id)

        response = requests.request("GET", url, headers=MailchimpHandler.HEADERS)

        json_data = json.loads(response.text)

        segments = json_data['segments']

        # if tag is found, return its id
        for segment in segments:
            if segment['name'] == name:
                return segment['id']

        # if not, returns false
        return False
