from django.views.decorators.csrf import csrf_exempt

from apps.cities.models import City
from apps.neighborhoods.models import Neighborhood
from rentalmoose.classes.API import *

# for protected views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny


# Create your views here.

@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def fetch_places(request, keyword):



    neighborhoods = Neighborhood.objects.filter(name__icontains=keyword).order_by('id')[:10:1]
    cities = City.objects.filter(name__icontains=keyword).order_by('id')[:10:1]


    return API.json_response(API.serialize_model_multiple([cities, neighborhoods]))
