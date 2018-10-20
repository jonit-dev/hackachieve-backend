from django.views.decorators.csrf import csrf_exempt

from apps.property_types.models import Property_type
from apps.users.models import User

from rentalmoose.classes.API import *

from rentalmoose.classes.PropertyHandler import *

# for protected views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


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
