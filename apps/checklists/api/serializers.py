from rest_framework import serializers
from apps.checklists.models import Checklist


class ChecklistSerializer(serializers.Serializer):
    description = serializers.CharField()
    status = serializers.BooleanField()
    user_id = serializers.IntegerField()
    goal_id = serializers.IntegerField()

    def create(self, validated_data):
        return Checklist.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.goal_id = validated_data.get('goal_id', instance.goal_id)

        instance.save()
        return instance
