from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from apps.columns.models import Column
from apps.users.models import User


class ColumnOrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Column
        fields = ['order_position', 'user']


class ColumnMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']


class ColumnMemberCreateSerializer(WritableNestedModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    member = ColumnMemberSerializer(many=True, required=False)

    class Meta:
        model = Column
        fields = ['id', 'member', 'user']
