from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from apps.neighborhoods.models import Neighborhood
from rentalmoose.classes.API import *

# for protected views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def fetch_neighborhoods(request,city_id, keyword):

    #fetch all neighborhoods with name containing something similar to the passed keyword
    neighborhoods = Neighborhood.objects.filter(name__icontains=keyword, city_id=city_id)

    return API.json_response(API.serialize_model(neighborhoods))




@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def has_neighborhoods(request,city_id):

    #fetch all neighborhoods with name containing something similar to the passed keyword
    neighborhoods = Neighborhood.objects.filter(city_id=city_id)

    if len(neighborhoods) > 0:
        return API.json_response({"hasNeighborhoods": True})
    else:
        return API.json_response({"hasNeighborhoods": False})



