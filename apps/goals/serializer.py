from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from apps.goals.models import Goal, GoalComment, CommentVote
from apps.projects.serializer import MemberDetialSerializer, FileSerializer
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class CreateNewGoalSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    deadline = serializers.DateTimeField(input_formats=['%Y-%M-%d'], required=False)
    description = serializers.CharField(required=False)

    class Meta:
        model = Goal
        fields = ['id', 'title', 'description', 'duration_hrs', 'deadline', 'column', 'priority', 'user']


class GoalSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    file = FileSerializer()

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
