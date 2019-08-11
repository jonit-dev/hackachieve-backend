import base64

from django.shortcuts import render

# Create your views here.
from drf_extra_fields.fields import Base64FileField
from requests.compat import basestring
from rest_framework import serializers, viewsets, parsers, status
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.base import ContentFile
from rest_framework.response import Response

from apps.documents.models import MediaFile
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'username']


class FileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = MediaFile
        fields = ['id', 'file', 'title', 'user']


class FileDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    file = serializers.SerializerMethodField('get_file_path')

    class Meta:
        model = MediaFile
        fields = ['id', 'file', 'title', 'user', 'timestamp']

    def get_file_path(self, obj):
        url = self.context.get('request').scheme + '://' + self.context.get('request').get_host() + obj.file.url
        return url


class FileView(viewsets.ModelViewSet):
    queryset = MediaFile.objects.all()
    serializer_class = FileSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = FileDetailSerializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = FileDetailSerializer(queryset, many=True)
        return Response(serializer.data)





