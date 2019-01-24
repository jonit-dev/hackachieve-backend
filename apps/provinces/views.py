from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from apps.cities.models import City
from hackachieve.classes.API import *

# for protected views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated



# CUSTOM VIEWS =========================== #

# ================================================================= #
#                      DASHBOARD
# ================================================================= #

# Protected view - dashboard
@csrf_exempt
@api_view(['GET'])
@permission_classes(())
def provinces_cities(request, id):
    cities = City.objects.filter(province_id=id)

    cities = serializers.serialize('json', cities)
    cities = json.loads(cities)

    #delete some extra useless data
    for city in cities:
        city['id'] = city['pk']
        del city['pk']
        del city['model']
        # city['province'] = city['fields']['province']
        city['name'] = city['fields']['name']
        del city['fields']

    return API.json_response({
     'cities': cities
    })
