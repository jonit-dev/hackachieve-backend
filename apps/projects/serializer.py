from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from django.forms.models import model_to_dict

from apps.projects.models import Project
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']


class ProjectCreateSerializer(WritableNestedModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    member = MemberSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'user', 'member']


class ProjectDetailSerializer(serializers.ModelSerializer):
    member = MemberSerializer(many=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'member', 'created_at']


class ProjectUpdateSerializer(WritableNestedModelSerializer):
    member = MemberSerializer(many=True)

    class Meta:
        model = Project
        fields = ['name', 'description', 'member']


class ProjectListSerializer(serializers.ModelSerializer):
    member = UserSerializer(many=True)
    user = UserSerializer()

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'member', 'user', 'member']
