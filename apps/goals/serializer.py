from rest_framework import serializers

from apps.goals.models import Goal, GoalComment, CommentVote


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'


class GoalPublicStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['is_public']


class GoalCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoalComment
        exclude = ('timestamp',)


class GoalCommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoalComment
        fields = '__all__'


class CommentVoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentVote
        fields = '__all__'


class GoalCommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoalComment
        fields = ['text']
