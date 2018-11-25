import urllib

from django.shortcuts import render

# Create your views here.
# for protected views
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rentalmoose.classes.API import *

import urllib


@csrf_exempt
@api_view(['GET'])
@permission_classes(())
def walkscore(request, address, lat, lng):
    walkscoreAPI = "6056fc826e5009f60e77752e88567bff"

    encoded_address = urllib.parse.quote(address)

    url = "http://api.walkscore.com/score?format=json&address=" + encoded_address + "&lat=" + lat + "&lon=" + lng + "&wsapikey=" + walkscoreAPI

    env = "prod"

    if env == "prod":
        f = urllib.request.urlopen(url)
        response = f.read()

        return HttpResponse(response, "json")
    else:
        response = {
            "status": 1,
            "walkscore": 0,
            "description": "Car-Dependent",
            "updated": "2018-10-31 15:38:48.287182",
            "logo_url": "https://cdn.walk.sc/images/api-logo.png",
            "more_info_icon": "https://cdn.walk.sc/images/api-more-info.gif",
            "more_info_link": "https://www.redfin.com/how-walk-score-works",
            "ws_link": "https://www.walkscore.com/score/13450-.dash.-104-Avenue-.dash.Surrey-BC/lat=53.7266683/lng=-127.6476205/?utm_source=live.com&utm_medium=ws_api&utm_campaign=ws_api",
            "help_link": "https://www.redfin.com/how-walk-score-works",
            "snapped_lat": 53.727,
            "snapped_lon": -127.647
        }
        return API.json_response(response)
