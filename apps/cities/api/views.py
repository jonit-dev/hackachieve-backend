from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from apps.cities.api.serializers import CitySerializer
from apps.cities.models import City

@permission_classes(())
class CityView(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    http_method_names = ['get']