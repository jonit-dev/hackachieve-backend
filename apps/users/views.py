import json
from threading import Thread

from django.contrib.auth import login
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.forms import model_to_dict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from requests.exceptions import HTTPError
from rest_framework import generics, status, views
# for protected views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from social_core.backends.oauth import BaseOAuth2
from social_core.exceptions import (AuthForbidden, AuthTokenError,
                                    MissingBackend)
from social_django.utils import load_backend, load_strategy

from hackachieve.classes.API import *
from hackachieve.classes.EmailHandler import EmailHandler
from hackachieve.classes.Environment import Environment
from hackachieve.classes.MailchimpHandler import MailchimpHandler
from hackachieve.classes.UserHandler import *
from hackachieve.classes.Validator import *
from django.db.models import Q

from .serializers import *


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
@api_view(['get'])
@permission_classes((IsAuthenticated,))
def search(request, keyword):
    user_id = API.getUserByToken(request)

    users = User.objects.filter(Q(email__icontains=keyword) | Q(first_name__icontains=keyword) | Q(last_name__icontains=keyword)).values()

    output = []
    for user in users:
        u = {
            'id': user['id'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'email': user['email']
        }
        output.append(u)

    return JsonResponse({"users": output})


@csrf_exempt
def user_register(request):
    if request.method == "POST":

        # get json data

        json_data = API.json_get_data(request)

        print(json_data)

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

            UserHandler.attach_area_of_knowledge(
                create_user, json_data['areas_of_knowledge'])

            # UserHandler.generate_initial_boards_columns(create_user)

            send = EmailHandler.send_email('Welcome to Hackachieve!', [json_data['email']],
                                           "welcome",
                                           {
                                               "name": json_data['firstName'],
                                               "login": json_data['email'],
                                               "password": json_data['password']
                                           })

            ENV = Environment.getkey('env')

            # Register on Mailchimp email list

            if ENV == "prod":  # only register on production
                # adjust firstname to first letter uppercase (eg. Joao)
                adjusted_name = json_data['firstName'].lower()
                adjusted_name = adjusted_name[:1].upper() + adjusted_name[1:]

                # add subscriber to our list

                t2 = Thread(target=MailchimpHandler.add_subscriber,
                            args=(json_data['email'], adjusted_name, json_data['lastName'], 'd3e968d31a'))
                t2.start()

                # add tags

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
                "message": "An error occurred while trying to create your new user. Please, contact our support.",
                "type": "danger"
            })

    else:
        response = {
            "error": "Invalid request"
        }
    return HttpResponse(json.dumps(response), content_type="application/json")


class SocialLoginView(generics.GenericAPIView):
    """Log in using facebook"""
    serializer_class = SocialSerializer
    permission_classes = [AllowAny]

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def post(self, request):
        """Authenticate user through the provider and access_token"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        provider = serializer.data.get('provider', None)
        strategy = load_strategy(request)

        try:
            backend = load_backend(strategy=strategy, name=provider,
                                   redirect_uri=None)

        except MissingBackend:
            return Response({'error': 'Please provide a valid provider'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            if isinstance(backend, BaseOAuth2):
                access_token = serializer.data.get('access_token')
            user = backend.do_auth(access_token)
        except HTTPError as error:
            return Response({
                "error": {
                    "access_token": "Invalid token",
                    "details": str(error)
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        except AuthTokenError as error:
            return Response({
                "error": "Invalid credentials",
                "details": str(error)
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            authenticated_user = backend.do_auth(access_token, user=user)

        except HTTPError as error:
            return Response({
                "error": "invalid token",
                "details": str(error)
            }, status=status.HTTP_400_BAD_REQUEST)

        except AuthForbidden as error:
            return Response({
                "error": "invalid token",
                "details": str(error)
            }, status=status.HTTP_400_BAD_REQUEST)

        if authenticated_user and authenticated_user.is_active:
            # generate JWT token
            login(request, authenticated_user)
            data = self.get_tokens_for_user(user)
            # customize the response to your needs
            response = {
                "email": authenticated_user.email,
                "username": authenticated_user.username,
                "token": data
            }
            return Response(status=status.HTTP_200_OK, data=response)
