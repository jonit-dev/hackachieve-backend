from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt

from apps.applications.models import Application
from apps.cities.models import City
from apps.neighborhoods.models import Neighborhood
from apps.property_types.models import Property_type
from apps.resumes_cities.models import Resume_city
from apps.resumes_neighborhoods.models import Resume_neighborhood
from apps.properties.models import Property
from apps.resumes.models import Resume
from apps.user_property_filter_property_types.models import User_property_filter_property_type
from rentalmoose.classes.API import *
from rentalmoose.classes.EmailHandler import *
from rentalmoose.classes.Validator import *
from rentalmoose.settings import HOST_NAME
from rentalmoose.classes.UserHandler import *
from rentalmoose.classes.SecurityHandler import *
from apps.user_property_filter.models import User_property_filter

# for protected views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

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

    # VALIDATION =========================== #

    # check if user has a resume
    if user.has_resume() == True:
        return API.json_response({
            "status": "error",
            "message": "This user already has a resume! Please, update it instead of creating a new one",
            "type": "danger"
        })

    # check if there's an empty field.
    request_fields = Validator.are_request_fields_valid(json_data)

    request_fields_valid = Validator.are_request_fields_valid(resume_data)

    if request_fields_valid is not True:
        return API.json_response({
            "status": "error",
            "message": "Error while trying to create your resume. The following fields are empty: {}".format(
                request_fields_valid),
            "type": "danger"
        })
    else:

        # create resume

        resume = Resume(
            tenant=user,
            phone=resume_data['phone'],
            description=resume_data['description'],
            expected_tenancy_length=resume_data['tenancyLength'],
            total_household_members=resume_data['totalHouseholdMembers'],
            consent_criminal_check=resume_data['consentCriminalCheck'],
            consent_credit_check=resume_data['consentCreditCheck'],
            eviction_history=resume_data['evictionHistory'],
            current_property_has_infestations=resume_data['currentPropertyInfestations'],
            has_pet=resume_data['hasPet'],
            currently_working=resume_data['working'],
            current_ocupation=resume_data['occupation'],
            maximum_rental_budget=resume_data['maximumRentalBudget'],
            total_household_income=resume_data['totalHouseholdIncome'],
            current_wage=resume_data['monthlyWage']
        )
        resume.save()

        if resume_data['rentAnywhere'] == False:
            # saving neighborhoods of interest
            if len(resume_data['neighborhoodsOfInterest']) > 0:
                for n in resume_data['neighborhoodsOfInterest']:
                    neighborhood = Neighborhood.objects.get(pk=n['id'])
                    rn = Resume_neighborhood(resume=resume, neighborhood=neighborhood)
                    rn.save()

            # saving cities of interest
            if len(resume_data['citiesOfInterest']) > 0:
                for n in resume_data['citiesOfInterest']:
                    city = City.objects.get(pk=n['id'])
                    rc = Resume_city(resume=resume, city=city)
                    rc.save()

        # User filter =========================== #

        filter = User_property_filter(resume=resume, max_budget=resume_data['maximumRentalBudget'], moving_date=None,
                                      rent_anywhere=resume_data['rentAnywhere'])
        filter.save()

        # attach properties types to filter (one (filter) to many (property types) relationship)
        for p in resume_data['propertyTypes']:
            property_type = Property_type.objects.get(pk=p['id'])
            user_property_filter_property_type = User_property_filter_property_type(property_filter=filter,
                                                                                    property_type=property_type)
            user_property_filter_property_type.save()

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

        ip = SecurityHandler.get_client_ip(request)

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

        # Check Landlord IP address =========================== #

        elif SecurityHandler.is_allowed_ip(ip, "CA") is False and json_data['type'] != 1:
            log = Log(
                event="SUSPICIOUS_ACCOUNT_CREATION_TRY", emitter=None, target=None, value=ip,
            )
            log.save()

            return API.json_response({
                "status": "error",
                "message": "Error while creating your account.",
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

            # adjust firstname to first letter uppercase (eg. Joao)
            adjusted_name = json_data['firstName'].lower()
            adjusted_name = adjusted_name[:1].upper() + adjusted_name[1:]

            send = EmailHandler.send_email('Welcome to RentalMoose', [json_data['email']],
                                           "welcome",
                                           {
                                               "name": adjusted_name,
                                               "login": json_data['email'],
                                               "password": json_data['password']

                                           })

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

from apps.logs.models import Log
from rentalmoose.classes.SecurityHandler import *


@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def user_info(request):
    user_id = API.getUserByToken(request)

    user = User.objects.get(pk=user_id)

    # get and register user IP
    ip = SecurityHandler.get_client_ip(request)
    log = Log(event="IP_ACCESS", emitter=user_id, target=None, value=ip)
    log.save()

    has_resume = len(user.resume_set.all()) > 0

    return API.json_response({
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_active': user.is_active,
        'type': user.type,
        'has_resume': has_resume
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

    if Application.objects.filter(resume=resume.id, property=property_id).count() > 0:
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

            # warn landlord about new application

            tenant_name = UserHandler.capitalize_name(tenant.first_name)
            landlord_name = UserHandler.capitalize_name(property.owner.first_name)

            send = EmailHandler.send_email('New applicant to ' +
                                           property.title, [property.owner.email],
                                           "apply_posting",
                                           {
                                               "tenant_application_link": "{}/property/check/applicants/{}/{}".format(
                                                   HOST_NAME, property_id, tenant.id),
                                               "property_title": property.title,
                                               "tenant_name": tenant_name,
                                               "landlord_first_name": landlord_name
                                           })

            return API.json_response({
                "status": "success",
                "message": "Your tenant's application resume was sent succesfully.",
                "type": "success"
            })
        else:
            return API.json_response({
                "status": "error",
                "message": "You don't have a registered resume to apply.",
                "type": "danger"
            })




    except ObjectDoesNotExist as e:  # and more generic exception handling on bottom
        return API.json_response({

            "status": "error",
            "message": "The property that you're trying to apply for does not exist.",
            "type": "danger"
        })
