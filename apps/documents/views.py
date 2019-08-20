import base64

from django.shortcuts import render

# Create your views here.
from rest_framework import serializers, viewsets, status
from rest_framework.mixins import DestroyModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

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


class DeleteFileView(DestroyModelMixin, GenericViewSet):
    queryset = MediaFile.objects.all()
    serializer_class = FileSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'File Delete Successfully'}, status=status.HTTP_204_NO_CONTENT)

