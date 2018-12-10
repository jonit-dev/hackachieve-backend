from rest_framework import serializers
from apps.cities.models import City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name', 'province')