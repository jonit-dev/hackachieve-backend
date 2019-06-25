from rest_framework import serializers

from apps.columns.models import Column


class ColumnOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ['order_position']