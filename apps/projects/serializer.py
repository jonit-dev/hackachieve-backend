from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from django.forms.models import model_to_dict

from apps.boards.models import Board
from apps.columns.models import Column
from apps.goals.models import Goal
from apps.labels.models import Label
from apps.projects.models import Project
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class LabelContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Label
        fields = ['id', 'name']


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


class ProjectContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description']


class BoardContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'name', 'description']


class ColumnContentSerializer(serializers.ModelSerializer):
    deadline = serializers.DateTimeField()

    class Meta:
        model = Column
        fields = ['id', 'name', 'description', 'deadline', 'order_position']


class GoalContentSerializer(serializers.ModelSerializer):
    deadline = serializers.DateTimeField()
    labels = LabelContentSerializer(many=True)

    class Meta:
        model = Goal
        fields = ['id', 'title', 'description', 'deadline', 'order_position', 'duration_hrs', 'priority', 'status',
                  'is_public', 'labels']


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
