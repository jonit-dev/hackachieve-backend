from rest_framework import viewsets, permissions

# SERIALIZER VIEW
from apps.provinces.api.serializers import ProvinceSerializer
from apps.provinces.models import Province


class ProvinceView(viewsets.ModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    http_method_names = ['get']
    permission_classes = (())