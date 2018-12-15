import time

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rentalmoose.classes.API import *

from rentalmoose.classes.EmailHandler import *


@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def email_threading(request):

    send = EmailHandler.send_email('Welcome to RentalMoose', ["therentalmoose@gmail.com"],
                              "welcome",
                              {
                                  "name": "rental",
                                  "login": "moose",
                                  "password": "123"

                              })


    return API.json_response({
        "status": "success",
        "message": "Your property was listed successfully!",
        "type": "success",
        "title": "Success"
    })
