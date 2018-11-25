from django.shortcuts import render

# Create your views here.
# for protected views
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rentalmoose.classes.API import *

import urllib.request as urllib


@csrf_exempt
@api_view(['GET'])
@permission_classes(())
def walkscore(request, address, lat, lng):
    walkscoreAPI = "6056fc826e5009f60e77752e88567bff"

    url = "http://api.walkscore.com/score?format=json&address={}&lat={}&lon={}&wsapikey={}".format(address, lat, lng,
                                                                                                   walkscoreAPI)

    f = urllib.urlopen(url)
    response = f.read()

    return HttpResponse(response,"json")
