from rest_framework import serializers

from apps.goals.models import Goal


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'
