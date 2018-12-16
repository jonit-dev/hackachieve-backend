import time

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rentalmoose.classes.API import *

from rentalmoose.classes.EmailHandler import *
from rentalmoose.classes.SecurityHandler import *

@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def ipcheck(request):


    check = SecurityHandler.is_allowed_ip("23.248.181.255", "CA","BC")

    if check:
        return API.json_response({
            "status": "allowed_ip"
        })
    else:
        return API.json_response({
            "status": "forbidden_ip"
        })\


@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def phonecheck(request):

    check = SecurityHandler.is_allowed_phone("7788467427", "BC", "CA")

    if check:
        return API.json_response({
            "status": "allowed_phone"
        })
    else:
        return API.json_response({
            "status": "forbidden_phone"
        })

#
# @csrf_exempt
# @api_view(['GET'])
# @permission_classes((AllowAny,))
# def email_threading(request):
#
#     send = EmailHandler.send_email('Welcome to RentalMoose', ["therentalmoose@gmail.com"],
#                               "welcome",
#                               {
#                                   "name": "rental",
#                                   "login": "moose",
#                                   "password": "123"
#
#                               })
#
#
#     return API.json_response({
#         "status": "success",
#         "message": "Your property was listed successfully!",
#         "type": "success",
#         "title": "Success"
#     })
