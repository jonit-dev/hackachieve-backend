from rest_framework import serializers

from apps.goals.models import Goal


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'


class GoalPublicStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['is_public']


class GoalOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['order_position']
