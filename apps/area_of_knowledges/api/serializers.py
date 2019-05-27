from rest_framework import serializers

from apps.area_of_knowledges.models import Area_of_knowledge


class AreaOfKnowledgeSerializer(serializers.Serializer):
    name = serializers.CharField()

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        aok_name = str(validated_data['name']).lower().capitalize()

        # verify if area of knowledge with same name already exists (case insensitive)
        aok_check = Area_of_knowledge.objects.filter(name__exact=aok_name)

        # if exists, attach to request user
        if aok_check.exists():
            print('AOK already exists, attaching to user...')
            user.areas_of_knowledge.add(aok_check.first())
            user.save()

            return aok_check.first()

        else:
            print('AOK does not exists. Creating new one')
            # if not, create a new one

            aok = Area_of_knowledge(
                user=user,
                name=aok_name
            )
            aok.save()

            # and attach to user
            print('And then attach to user!')
            user.areas_of_knowledge.add(aok)
            user.save()

            return aok

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
