from rest_framework import viewsets, permissions

from apps.countries.api.serializers import CountrySerializer
from apps.countries.models import Country


class CountryView(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    http_method_names = ['get']
