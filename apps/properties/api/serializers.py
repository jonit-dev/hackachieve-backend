from rest_framework import serializers
from apps.cities.models import City
from apps.properties.models import Property
from apps.property_types.models import Property_type


class PropertySerializer(serializers.ModelSerializer):
    # lets insert a custom field on the answer
    city_name = serializers.SerializerMethodField()
    type_name = serializers.SerializerMethodField()

    def get_city_name(self, obj):
        city = City.objects.get(pk=obj.city_id)
        return city.name

    def get_type_name(self, obj):
        type = Property_type.objects.get(pk=obj.type_id)
        return type.name

    class Meta:
        model = Property
        fields = (
            'id', 'owner_id', 'status', 'title', 'sqft', 'type_id', 'rental_value', 'utilities_included', 'n_bedrooms',
            'n_bathrooms', 'address', 'furnished', 'no_pets', 'no_smoking', 'no_parties', 'minimum_lease',
            'pet_deposit',
            'security_deposit', 'publication_date', 'available_to_move_in_date', 'open_view_start', 'open_view_end',
            'city_name', 'type_name')