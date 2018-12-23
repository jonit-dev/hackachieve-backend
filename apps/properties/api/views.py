from rest_framework import viewsets, permissions

from apps.properties.api.serializers import PropertySerializer
from apps.properties.models import Property

# SERIALIZER VIEW

class PropertyView(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    http_method_names = ['get','delete']
    permission_classes = (())