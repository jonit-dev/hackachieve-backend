from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.forms import model_to_dict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from hackachieve.classes.EmailHandler import EmailHandler
from hackachieve.classes.Validator import *
from hackachieve.classes.API import *
from hackachieve.classes.UserHandler import *

# for protected views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

import json
from django.core import serializers


@csrf_exempt
@api_view(['get'])
@permission_classes((IsAuthenticated,))
def info(request):
    user_id = API.getUserByToken(request)
    user = User.objects.get(pk=user_id)

    return API.json_response({
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email
    })


@csrf_exempt
def user_register(request):
    if request.method == "POST":

        # get json data

        json_data = API.json_get_data(request)

        # Empty fields valitation =========================== #

        check_user_fields = Validator.are_request_fields_valid(json_data)

        # Check is theres no empty fields
        if check_user_fields is not True:
            return API.json_response({
                "status": "error",
                "message": "Error while trying to create your account. The following fields are empty: {}".format(
                    check_user_fields),
                "type": "danger"
            })

        if Validator.check_user_exists(json_data['email']):
            return API.json_response({
                "status": "error",
                "message": "This e-mail is already registered in our system. Please, choose another one and try again.",
                "type": "danger"
            })

        else:  # if everything is ok, procceed

            # create user here

            create_user = User.objects.create_user(
                username=json_data['email'],
                email=json_data['email'],
                password=json_data['password'],
                first_name=json_data['firstName'],
                last_name=json_data['lastName']
            )

            # setup boards and columns

            # by default, user will have long term board / short term board and a Sprint, on going and backlog column for each

        # After user creation...

        if create_user:

            UserHandler.generate_initial_boards_columns(create_user)

            send = EmailHandler.send_email('Welcome to Hackachieve', [json_data['email']],
                                           "welcome",
                                           {
                                               "name": json_data['firstName'],
                                               "login": json_data['email'],
                                               "password": json_data['password']
                                           })

            # Register on maillist

            # adjust firstname to first letter uppercase (eg. Joao)
            # adjusted_name = json_data['firstName'].lower()
            # adjusted_name = adjusted_name[:1].upper() + adjusted_name[1:]

            # send = EmailHandler.send_email('Welcome to hackachieve', [json_data['email']],
            #                                "welcome",
            #                                {
            #                                    "name": adjusted_name,
            #                                    "login": json_data['email'],
            #                                    "password": json_data['password']
            #
            #                                })
            #
            # t2 = Thread(target=MailchimpHandler.add_subscriber,
            #             args=(json_data['email'], json_data['firstName'], json_data['lastName']))
            # t2.start()
            #
            # if json_data['type'] == 1:
            #     t3 = Thread(target=MailchimpHandler.attach_tags,
            #                 args=(['Tenant'], json_data['email']))
            #     t3.start()
            #
            # if json_data['type'] == 2:
            #     t3 = Thread(target=MailchimpHandler.attach_tags,
            #                 args=(['Landlord'], json_data['email']))
            #     t3.start()

            return API.json_response({
                "status": "success",
                "message": "Your account {} was created successfully! Redirecting...".format(json_data['email']),
                "type": "success"
            })
        else:
            return API.json_response({
                "status": "error",
                "message": "An error occured while trying to create your new user. Please, contact our support.",
                "type": "danger"
            })

    else:
        response = {
            "error": "Invalid request"
        }
    return HttpResponse(json.dumps(response), content_type="application/json")
