from rest_framework import serializers
from rest_framework.response import Response

from apps.goals.models import Goal
from apps.labels.models import Label


class LabelSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField()
    user_id = serializers.IntegerField(required=False)

    def create(self, validated_data):
        request = self.context['request']
        pk = self.context['pk']
        user = request.user

        # lets check if label already exists

        check_label = Label.objects.filter(name=validated_data['name'], user=user).first()
        label_exists = Label.objects.filter(name=validated_data['name'], user=user).exists()

        if not label_exists:

            # print('>>> Label does not exists. CREATING')

            # if label doesnt exists, create it
            label = Label(
                user=user,
                name=validated_data['name']
            )
            label.save()

            # and then attach to the user goal

            # print('>>> Attaching to goal')
            goal = Goal.objects.get(pk=pk)
            goal.labels.add(label)
            goal.save()

            return label
        else:  # if label exists

            print('>>> Label exists, attaching to goal')

            # just attach to user


            goal = Goal.objects.get(pk=pk, user=user)
            goal.labels.add(check_label)
            goal.save()

            return check_label

    def update(self, instance, validated_data):
        request = self.context['request']
        user = request.user

        instance.name = validated_data.get('name', instance.name)

        instance.save()
        return instance
