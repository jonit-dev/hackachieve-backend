from rest_framework import viewsets, permissions

from apps.cities.models import City
from apps.countries.models import Country
from apps.properties.models import Property
from apps.provinces.models import Province
from apps.resumes.models import Resume

from rentalmoose.serializers import ProvinceSerializer, CitySerializer, ResumeSerializer, CountrySerializer, \
    PropertySerialier


# SERIALIZER VIEWS =========================== #

class PropertyView(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerialier


class ProvinceView(viewsets.ModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer


class CityView(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class ResumeView(viewsets.ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer


class CountryView(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
