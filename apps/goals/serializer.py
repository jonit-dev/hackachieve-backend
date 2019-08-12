from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from apps.goals.models import Goal, GoalComment, CommentVote
from apps.projects.serializer import MemberDetialSerializer
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class GoalSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Goal
        fields = '__all__'


class GoalPublicStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['is_public']


class GoalCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = GoalComment
        fields = ['id', 'text', 'user']


class GoalCommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalComment
        fields = ['id', 'goal', 'text', 'user']


class GoalCommentDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = GoalComment
        fields = ['text', 'user']


class CommentVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentVote
        fields = '__all__'


class GoalCommentUpdateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalComment
        fields = ['text', 'user']


class GoalOrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        fields = ['order_position', 'user']


class UpdateGoalFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['file']


class GoalMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']


class GoalcreateSerializer(WritableNestedModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    member = GoalMemberSerializer(many=True, required=False)

    class Meta:
        model = Goal
        fields = ['id', 'member', 'user']


class GoalMemberDetailSerializer(serializers.ModelSerializer):
    member = MemberDetialSerializer(many=True)

    class Meta:
        model = Goal
        fields = ['id', 'member']
