from rest_framework import serializers

from apps.checklists.models import Checklist
from apps.goals.models import Goal


class ChecklistSerializer(serializers.Serializer):
    description = serializers.CharField()
    status = serializers.BooleanField()
    goal_id = serializers.IntegerField()

    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        checklist = Checklist(
            user=user,
            goal=Goal.objects.get(pk=validated_data['goal_id']),
            status=validated_data['status'],
            description=validated_data['description']
        )
        checklist.save()

        return checklist

    def update(self, instance, validated_data):
        request = self.context['request']
        user = request.user

        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        instance.user = user
        instance.goal_id = validated_data.get('goal_id', instance.goal_id)

        instance.save()
        return instance


