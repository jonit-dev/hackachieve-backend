from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from apps.columns.models import Column
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


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


class ColumnSerializer(serializers.ModelSerializer):
    user = UserSerializer

    class Meta:
        model = Column
        fields = "__all__"

