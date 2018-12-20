import urllib

from django.shortcuts import render

# Create your views here.
# for protected views
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rentalmoose.classes.API import *
from rentalmoose.classes.Environment import *
import urllib


@csrf_exempt
@api_view(['GET'])
@permission_classes(())
def walkscore(request, address, lat, lng):
    env = Environment.getkey('env')
    walkscoreAPIKEY = Environment.getkey('walkscore')

    encoded_address = urllib.parse.quote(address)

    url = "http://api.walkscore.com/score?format=json&address=" + encoded_address + "&lat=" + lat + "&lon=" + lng + "&transit=1&bike=1&wsapikey=" + walkscoreAPIKEY

    if env == "prod":
        f = urllib.request.urlopen(url)
        response = f.read()

        return HttpResponse(response, "json")
    else:
        response = {
    "status": 1,
    "walkscore": 61,
    "description": "Somewhat Walkable",
    "updated": "2018-11-28 21:05:32.266310",
    "logo_url": "https://cdn.walk.sc/images/api-logo.png",
    "more_info_icon": "https://cdn.walk.sc/images/api-more-info.gif",
    "more_info_link": "https://www.redfin.com/how-walk-score-works",
    "ws_link": "https://www.walkscore.com/score/W-939-58th-Oakridge/lat=49.217810/lng=-123.116010/?utm_source=rentalmoose.ca &utm_medium=ws_api&utm_campaign=ws_api",
    "help_link": "https://www.redfin.com/how-walk-score-works",
    "snapped_lat": 49.218,
    "snapped_lon": -123.1155,
    "transit": {
        "score": None,
        "description": None,
        "summary": None
    },
    "bike": {
        "score": 65,
        "description": "Bikeable"
    }
}
        return API.json_response(response)
