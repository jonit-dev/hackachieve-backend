from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Property_type
from rentalmoose.classes.API import *


@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def fetch_types(request):
    types = Property_type.objects.all()

    return API.json_response(API.serialize_model(types))

