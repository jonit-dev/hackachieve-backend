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
def fetch_neighborhoods(request,keyword):

    #fetch all neighborhoods with name containing something similar to the passed keyword

    neighborhoods = Neighborhood.objects.filter(name__icontains=keyword)

    return API.json_response(API.serialize_model(neighborhoods))
