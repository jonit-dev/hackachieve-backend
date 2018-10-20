from django.views.decorators.csrf import csrf_exempt

from apps.properties.models import Property
from apps.property_types.models import Property_type
from apps.users.models import User
from rentalmoose.classes.API import *

# for protected views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

import base64
from django.core.files.base import ContentFile


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create(request):
    request_data = API.json_get_data(request)


    #Lets find the who is the owner of this property listing, from the incoming POST request
    owner_id = API.getUserByToken(request)
    owner = User.objects.get(pk=owner_id)

    #Set property type

    property_type = Property_type.objects.get(pk=request_data['type_id'])


    # Convert file information (get from base64 and convert to fileContent
    format, imgstr = request_data['image'].split(';base64,')
    ext = format.split('/')[-1]
    data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)  # You can save this as file instance.

    property = Property(
        owner_id=owner,
        status=request_data['status'],
        title=request_data['title'],
        sqft=request_data['sqft'],
        type_id=property_type,
        rental_value=request_data['rental_value'],
        utilities_included=request_data['utilities_included'],
        n_bedrooms=request_data['n_bedrooms'],
        n_bathrooms=request_data['n_bathrooms'],
        address=request_data['address'],
        furnished=request_data['furnished'],
        no_pets=request_data['no_pets'],
        no_smoking=request_data['no_smoking'],
        no_parties=request_data['no_parties'],
        minimum_lease=request_data['minimum_lease'],
        pet_deposit=request_data['pet_deposit'],
        security_deposit=request_data['security_deposit'],
        publication_date=request_data['publication_date'],
        available_to_move_in_date=request_data['available_to_move_in_date'],
        open_view_start=request_data['open_view_start'],
        open_view_end=request_data['open_view_end'],
        upload=data

    )
    property.save()

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
