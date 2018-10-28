from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt

from apps.applications.models import Application
from apps.cities.models import City
from apps.properties.models import Property
from apps.resumes.models import Resume
from rentalmoose.classes.API import *
from rentalmoose.classes.Validator import *

# for protected views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

import json
from django.core import serializers


# CUSTOM VIEWS =========================== #

# ================================================================= #
#                      DASHBOARD
# ================================================================= #

# Protected view - dashboard
@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def user_dashboard(request):
    user_id = API.getUserByToken(request)

    user = User.objects.get(pk=user_id)

    user_resumes = user.resume_set.all()

    has_resumes = len(user_resumes)

    has_resumes = has_resumes > 0

    if has_resumes is not True:

        # if user does not have resume, lets force him to register one.

        # user_resumes = serializers.serialize('json', user_resumes)

        return API.json_response({
            'has_resumes': has_resumes,
            # 'user_resumes': json.loads(user_resumes)
            # you MUST use a json.loads here to load the serialized json model. Otherwise, it wont work!
        })
    else:

        # if the user has a resume registered, let him see all properties

        # CUSTOM JSON SERIALIZER =========================== #

        properties = Property.objects.all()

        # data is a python list
        data = json.loads(serializers.serialize('json', properties))

        final_results = []
        for d in data:
            d['fields']['owner_name'] = User.objects.get(pk=d['fields']['owner']).first_name
            d['fields']['id'] = d['pk']
            del d['fields']['owner']
            del d['pk']
            del d['model']
            d = d['fields']
            final_results.append(d)

        d = {}
        d = final_results
        return HttpResponse(json.dumps(d), content_type="application/json")


# ================================================================= #
#                      RESUME
# ================================================================= #

@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def resume_create(request):
    # get user
    user_id = API.getUserByToken(request)
    user = User.objects.get(pk=user_id)

    resume_data = API.json_get_data(request)

    json_data = API.json_get_data(request)
    city_id = json_data['city']['id']
    city = City.objects.get(pk=city_id)

    request_fields = Validator.are_request_fields_valid(json_data)

    request_fields_valid = Validator.are_request_fields_valid(resume_data)

    if request_fields_valid is not True:
        return API.json_response({
            "status": "error",
            "message": "Error while trying to create your resume. The following fields are empty: {}".format(
                ", ".join(request_fields_valid)),
            "type": "danger"
        })

    elif user.has_resume() == True:

        # update resume data
        # todo: update resume

        return API.json_response({
            "status": "error",
            "message": "This user already has a resume! Please, update it instead of creating a new one",
            "type": "danger"
        })
    else:

        # create resume

        resume = Resume(
            tenant=user,
            city=city,
            phone=resume_data['phone'],
            description=resume_data['description'],
            zipcode=resume_data['zipcode'],
            address=resume_data['address'],
            expected_tenancy_length=resume_data['tenancyLength'],
            total_household_members=resume_data['totalHouseholdMembers'],
            consent_criminal_check=resume_data['consentCriminalCheck'],
            eviction_history=resume_data['evictionHistory'],
            current_property_has_infestations=resume_data['currentPropertyInfestations'],
            has_pet=resume_data['hasPet'],
            currently_working=resume_data['working'],
            current_ocupation=resume_data['occupation'],
            credit_score=resume_data['creditScore'],
            maximum_rental_budget=resume_data['maximumRentalBudget'],
            current_wage=resume_data['monthlyWage']
        )
        resume.save()

        if resume:
            return API.json_response({
                "status": "success",
                "message": "Your resume was created successfully",
                "type": "success"
            })
        else:
            return API.json_response({
                "status": "error",
                "message": "Error while trying to register your resume. Please, contact our support team.",
                "type": "danger"
            })


# ================================================================= #
#                      REGISTER
# ================================================================= #

@csrf_exempt
def user_register(request):
    if request.method == "POST":

        # get json data

        json_data = API.json_get_data(request)

        # Empty fields valitation =========================== #

        check_user_fields = Validator.are_request_fields_valid(json_data)

        if check_user_fields is not True:
            return API.json_response({
                "status": "error",
                "message": "Error while trying to create your account. The following fields are empty: {}".format(
                    ", ".join(check_user_fields)),
                "type": "danger"
            })
        elif not Validator.check_password_confirmation(json_data['password'], json_data['passwordConfirmation']):
            return API.json_response({
                "status": "error",
                "message": "Your password does not match its respective password confirmation. Please, try again.",
                "type": "danger"
            })
        elif Validator.check_user_exists(json_data['email']):
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
                last_name=json_data['lastName'],
                type=json_data['type']
            )

        if create_user:
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


# ================================================================= #
#                      GET OWN INFO
# ================================================================= #

@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def user_info(request):
    user_id = API.getUserByToken(request)

    user = User.objects.get(pk=user_id)
    return API.json_response({
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_active': user.is_active,
        'type': user.type
    })


# ================================================================= #
#                      APPLY FOR A PROPERTY
# ================================================================= #

@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def user_apply(request, property_id):
    # get the property name that we want to apply for

    # Validation =========================== #

    # check if its a tenant who's applying for it
    tenant = User.objects.get(pk=API.getUserByToken(request))

    if tenant.type != 1:
        return API.json_response({
            "status": "error",
            "message": "Sorry. Only tenants can apply for properties.",
            "type": "danger"
        })

    resume_query = tenant.resume_set.filter(active=True)
    resume = resume_query.first()
    resume_count = resume_query.count()

    if Application.objects.filter(resume=resume.id,property=property_id).count() > 0:
        return API.json_response({
            "status": "error",
            "message": "You already sent a resume for this application",
            "type": "danger"
        })


    # Application =========================== #

    try:
        property = Property.objects.get(pk=property_id)



        if resume_count >= 1:
            Application.apply(resume, property)

            return API.json_response({
                "status": "success",
                "message": "Your tenant's application resume was sent.",
                "type": "success"
            })
        else:
            return API.json_response({
                "status": "error",
                "message": "You dont have a registered resume to apply.",
                "type": "danger"
            })




    except ObjectDoesNotExist as e:  # and more generic exception handling on bottom
        return API.json_response({

            "status": "error",
            "message": "The property that you're trying to apply for does not exist.",
            "type": "danger"
        })
