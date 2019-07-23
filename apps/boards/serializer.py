from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from apps.boards.models import Board
from apps.columns.models import Column
from apps.goals.models import Goal, GoalComment
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']


class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'name', 'description']


class LongTermSerializer(serializers.ModelSerializer):
    member = UserSerializer(many=True)

    class Meta:
        model = Column
        fields = ['id', 'name', 'description', 'deadline', 'order_position', 'member']


class GoalCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = GoalComment
        fields = ['text', 'user', 'timestamp']


class ShortTermSerializer(serializers.ModelSerializer):
    member = UserSerializer(many=True)

    class Meta:
        model = Goal
        fields = ['id', 'title', 'description', 'order_position', 'deadline', 'priority', 'status',
                  'duration_hrs', 'is_public', 'member']
