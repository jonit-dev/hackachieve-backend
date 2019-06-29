from rest_framework import serializers

from apps.columns.models import Column


class ColumnOrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Column
        fields = ['order_position', 'user']