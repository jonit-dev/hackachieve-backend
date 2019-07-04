from rest_framework import serializers

from apps.projects.models import Project
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProjectCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Project
        fields = ['name', 'description', 'user']


class ProjectDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Project
        fields = ['name', 'description', 'user', 'created_at']


class ProjectUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['name', 'description']
