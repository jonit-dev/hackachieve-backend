import time

from apps.neighborhoods.models import Neighborhood
from apps.resumes_cities.models import Resume_city
from apps.resumes_neighborhoods.models import Resume_neighborhood
from apps.users.models import User
from rentalmoose.classes.MailchimpHandler import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rentalmoose.classes.API import *

from rentalmoose.classes.EmailHandler import *
from rentalmoose.classes.SecurityHandler import *


@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def mailchimp(request):
    # get all users
    users = User.objects.all()

    for user in users:
        print("Processing user {}".format(user))

        t2 = Thread(target=MailchimpHandler.add_subscriber,
                    args=(user.email, user.first_name, user.last_name))
        t2.start()


        if user.type is 1:
            t3 = Thread(target=MailchimpHandler.attach_tags,
                        args=(['Tenant'], user.email))
            t3.start()
        if user.type is 2:
            t5 = Thread(target=MailchimpHandler.attach_tags,
                        args=(['Landlord'], user.email))
            t5.start()

        # check if has resume

        if len(user.resume_set.all()) is not 0:
            resume_id = user.resume_set.first().id
            print("resume_id: {}".format(resume_id))

            resume_cities = Resume_city.objects.filter(resume=int(resume_id))
            cities_tags = []
            for resume_city in resume_cities:
                cities_tags.append(resume_city.city.name)

            t1 = Thread(target=MailchimpHandler.attach_tags,
                        args=(cities_tags, user.email))
            t1.start()

            resume_neighborhoods = Resume_neighborhood.objects.filter(resume=int(resume_id))
            neighborhood_tags = []
            for resume_neighborhood in resume_neighborhoods:
                neighborhood_tags.append(resume_neighborhood.neighborhood.name)

            t2 = Thread(target=MailchimpHandler.attach_tags,
                        args=(neighborhood_tags, user.email))
            t2.start()


        else:
            continue

    return API.json_response({
        "status": "subscribers processed"
    })

# @csrf_exempt
# @api_view(['GET'])
# @permission_classes((AllowAny,))
# def ipcheck(request):
#
#
#     check = SecurityHandler.is_allowed_ip("23.248.181.255", "CA","BC")
#
#     if check:
#         return API.json_response({
#             "status": "allowed_ip"
#         })
#     else:
#         return API.json_response({
#             "status": "forbidden_ip"
#         })\
#
#
# @csrf_exempt
# @api_view(['GET'])
# @permission_classes((AllowAny,))
# def phonecheck(request):
#
#     check = SecurityHandler.is_allowed_phone("7777777777", "BC", "CA")
#
#     if check:
#         return API.json_response({
#             "status": "allowed_phone"
#         })
#     else:
#         return API.json_response({
#             "status": "forbidden_phone"
#         })

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
