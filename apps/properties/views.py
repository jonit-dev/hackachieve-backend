from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt

from apps.property_types.models import Property_type
from apps.users.models import User

from rentalmoose.classes.API import *

from rentalmoose.classes.PropertyHandler import *
from rentalmoose.classes.ResumeHandler import *

# for protected views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from apps.applications.models import Application


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create(request):
    # get data coming in JSON format
    request_data = API.json_get_data(request)

    # Lets find the who is the owner of this property listing, from the incoming POST request
    owner_id = API.getUserByToken(request)
    owner = User.objects.get(pk=owner_id)

    # Set property type
    property_type = Property_type.objects.get(pk=request_data['type_id'])

    # Convert file information (get from base64 and convert to fileContent
    img_data = PropertyHandler.get_base64_img_data(request_data['image'])

    # Before saving the file, lets verify if its a allowed file type
    check_allowed_file_extension = PropertyHandler.check_file_extensions(img_data['ext'])

    if check_allowed_file_extension:

        # save property on DB
        property = PropertyHandler.save_property(request_data, owner, property_type, img_data)

        # now lets move the image files that were created to the respective property folder (static/images/properties)
        PropertyHandler.reallocate_uploaded_files(property, img_data)

        if property:
            return API.json_response({
                "status": "success",
                "message": "Your property was listed successfully!",
                "type": "success"
            })
        else:
            return API.json_response({
                "status": "error",
                "message": "Error while trying to list your property. Please, contact our support.",
                "type": "danger"
            })
    else:
        return API.json_response({
            "status": "error",
            "message": "The file extension that you're trying to submit is not allowed. Please, send a .png, .jpg or .bmp image file",
            "type": "danger"
        })


@csrf_exempt
@api_view(['GET'])
@permission_classes(())
def show_dashboard(request):
    properties = Property.objects.all()[:3]

    return API.json_response(API.serialize_model(properties))


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
@permission_classes(())
def applications(request, id):
    # Validation =========================== #

    user = User.objects.get(pk=API.getUserByToken(request))
    property = Property.objects.get(pk=id)

    # check if user is a landlord
    if user.type is not 2:
        return API.json_response({
            "status": "error",
            "message": "Only landlords are allowed to access this information.",
            "type": "danger"
        })

    # check if user is the owner of this property
    elif property.owner_id != user.id:
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
                scores = []

                for application in applications:

                    resume = application.resume.get()

                    if resume.active:
                        scores.append(ResumeHandler.calculate_risk(resume, property))


                return HttpResponse(json.dumps(scores), content_type="application/json")

        except ObjectDoesNotExist as e:

            return API.json_response({
                "status": "error",
                "message": "This property does not exists.",
                "type": "danger"
            })
