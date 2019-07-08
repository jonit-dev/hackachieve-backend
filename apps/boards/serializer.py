from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from apps.boards.models import Board
from apps.columns.models import Column
from apps.goals.models import Goal
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
    class Meta:
        model = Column
        fields = ['id', 'name', 'description', 'deadline', 'order_position']


class ShortTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['id', 'title', 'description', 'order_position', 'deadline', 'priority', 'status',
                  'duration_hrs', 'is_public']
