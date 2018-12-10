from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.cities.api.serializers import CitySerializer
from apps.cities.models import City

class CityView(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    http_method_names = ['get']
    permission_classes = (AllowAny,)
