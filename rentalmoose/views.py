from rest_framework import viewsets, permissions

from apps.cities.models import City
from apps.countries.models import Country
from apps.properties.models import Property
from apps.provinces.models import Province
from apps.resumes.models import Resume

from rentalmoose.serializers import  CitySerializer, ResumeSerializer, CountrySerializer


# SERIALIZER VIEWS =========================== #




class CityView(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    http_method_names = ['get']

class ResumeView(viewsets.ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    http_method_names = ['get']


class CountryView(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    http_method_names = ['get']