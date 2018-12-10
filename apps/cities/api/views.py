from rest_framework import viewsets, permissions

from apps.cities.api.serializers import CitySerializer
from apps.cities.models import City


class CityView(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    http_method_names = ['get']
    permission_classes = (())