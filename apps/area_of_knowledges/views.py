from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

# Create your views here.
from apps.area_of_knowledges.models import Area_of_knowledge
from hackachieve.classes.API import API


@csrf_exempt
@api_view(['get'])
@permission_classes((IsAuthenticated,))
def keyword(request, keyword):
    aoks = Area_of_knowledge.objects.filter(name__icontains=keyword)

    #get this model using a filter
    aoks = list(aoks.values())

    return JsonResponse(aoks, safe=False)
