from django.views.decorators.csrf import csrf_exempt

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
    owner_id = request_data['owner_id']

    format, imgstr = request_data['image'].split(';base64,')
    ext = format.split('/')[-1]

    data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)  # You can save this as file instance.


    return API.json_response({
        "owner_id": owner_id
    })
