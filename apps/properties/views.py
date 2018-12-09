from operator import itemgetter

import time
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt

from apps.cities.models import City
from apps.neighborhoods.models import Neighborhood
from apps.property_types.models import Property_type
from apps.users.models import User
from apps.properties.models import Property

from rentalmoose.classes.API import *

from rentalmoose.classes.PropertyHandler import *
from rentalmoose.classes.ResumeHandler import *

# for protected views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from apps.applications.models import Application
from rentalmoose.classes.UserHandler import UserHandler

from rentalmoose.classes.Validator import Validator


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create(request):
    # get data coming in JSON format
    request_data = API.json_get_data(request)

    # first of all, lets check if all request fields were filled properly

    check_fields = Validator.are_request_fields_valid(request_data)

    if check_fields is not True:

        return API.json_response({
            "status": "error",
            "message": "The following fields are empty: {}".format(check_fields),
            "type": "error",
            "title": "Error"
        })

    else:

        # Lets find the who is the owner of this property listing, from the incoming POST request
        owner_id = API.getUserByToken(request)
        owner = User.objects.get(pk=owner_id)

        # Validation =========================== #

        # check if user who's trying to list a property is a landlord

        if owner.type != 2:
            return API.json_response({
                "status": "error",
                "message": "Only landlords accounts can list real estate properties.",
                "type": "danger"
            })

        # SAVE PROPERTY FIRST!
        property_type = Property_type.objects.get(pk=request_data['type_id'])
        property = PropertyHandler.save_property(request_data, owner, property_type)

        # now that the property is saved, create folder on static dir to save uploaded images
        property_id = str(property.id)

        image_path = settings.PROPERTIES_IMAGES_ROOT + "/" + property_id

        def supermakedirs(path, mode):
            if not path or os.path.exists(path):
                return []
            (head, tail) = os.path.split(path)
            res = supermakedirs(head, mode)
            os.mkdir(path)
            os.chmod(path, mode)
            res += [path]
            return res

        if not os.path.isdir(image_path):
            path = os.path.join(image_path)
            supermakedirs(path, 0o775)

        i = 0
        for image in request_data['images']:
            img_data = PropertyHandler.get_base64_img(image["image"])

            if PropertyHandler.check_file_extensions(img_data['ext']):  # if file has allowed extension

                while True:  # save it!

                    time.sleep(0.2)
                    if os.path.isdir(image_path):  # we have to check if directory is created, because its async
                        # when the directory is created, create image file there.
                        image_file = open("{}/{}.{}".format(image_path, i, img_data['ext']), "wb")  # save file
                        image_file.write(img_data['base64data'])  # write base64 content
                        image_file.close()
                        i = i + 1  # now lets save the next file!

                        break

        return API.json_response({
            "status": "success",
            "message": "Your property was listed successfully!",
            "type": "success",
            "title": "Success"
        })


@csrf_exempt
@api_view(['GET'])
@permission_classes(())
def show_dashboard(request):
    properties = Property.objects.all()[:3]

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


@csrf_exempt
@api_view(['GET'])
@permission_classes(())
def show(request, id):
    try:

        # try to find the property and return it
        property = Property.objects.filter(pk=id)
        return API.json_response(API.serialize_model(property)[0])

    except Exception as e:  # if not found, display this message
        return API.json_response({
            "status": "error",
            "message": "Real estate property not found.",
            "type": "danger"
        })


@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def applicant_info(request, property_id, applicant_id):
    # VALIDATION =========================== #

    user_id = API.getUserByToken(request)

    # check if the user that's making the request is a landlord
    user = User.objects.get(pk=user_id)
    if not UserHandler.is_landlord(user):
        return API.json_response({
            "status": "error",
            "message": "You must be a landlord to do this request.",
            "type": "danger"
        })

    # check if user owns this property
    property = Property.objects.get(pk=property_id)
    # print("PROPERTYOWNER={} - USER_ID={}".format(property.owner_id, user.id))

    if PropertyHandler.is_owner(property, user) is False:
        return API.json_response({
            "status": "error",
            "message": "You cannot access applications from properties that are not yours.",
            "type": "danger"
        })

    # FETCH APPLICATIONS =========================== #

    # fetch all applications from a especific property

    applications = property.application_set.all()

    for application in applications:
        resume = application.resume.get()

        if resume.tenant_id == int(applicant_id):
            return API.json_response(ResumeHandler.calculate_risk(resume, property, application))

    return API.json_response({
        "status": "error",
        "message": "Application not found.",
        "type": "danger"
    })


@csrf_exempt
@api_view(['GET'])
@permission_classes(())
def applications(request, property_id):
    # Validation =========================== #

    user = User.objects.get(pk=API.getUserByToken(request))
    property = Property.objects.get(pk=property_id)

    # check if user is a landlord
    if not UserHandler.is_landlord(user):
        return API.json_response({
            "status": "error",
            "message": "Only landlords are allowed to access this information.",
            "type": "danger"
        })

    # check if user is the owner of this property
    elif PropertyHandler.is_owner(property, user) is False:
        return API.json_response({
            "status": "error",
            "message": "You cannot access applications from properties that are not yours.",
            "type": "danger"
        })

    else:

        try:

            applications = property.application_set.all()
            applications_count = applications.count()

            if applications_count == 0:
                return API.json_response({
                    "status": "error",
                    "message": "No one applied for this property yet.",
                    "type": "danger"
                })
            else:
                tenants_applications = []

                for application in applications:

                    resume = application.resume.get()

                    if resume.active:
                        tenants_applications.append(ResumeHandler.calculate_risk(resume, property, application))

                # returns response sorted by lowest score first (thats why we use itemgetter)
                return HttpResponse(json.dumps(sorted(tenants_applications, key=itemgetter('overallScore'))),
                                    content_type="application/json")

        except ObjectDoesNotExist as e:

            return API.json_response({
                "status": "error",
                "message": "This property does not exists.",
                "type": "danger"
            })


@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def properties_listing(request):
    owner_id = API.getUserByToken(request)

    properties = Property.objects.filter(owner=owner_id)

    properties = serializers.serialize('json', properties)

    # add additional field to response
    return API.json_response(API.clean_fields(properties, additional_fields=[
        {"key": "is_owner", "value": True}
    ]))
