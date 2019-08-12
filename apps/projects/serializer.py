from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
# from django.forms.models import model_to_dict
from apps.boards.models import Board
from apps.columns.models import Column
from apps.documents.models import MediaFile
from apps.goals.models import Goal
from apps.labels.models import Label
from apps.projects.models import Project
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class LabelContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'name']


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']


class MemberDetialSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'username']


class ProjectCreateSerializer(WritableNestedModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    member = MemberSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'user', 'member']


class ProjectContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description']


class FileSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField('get_file_path')

    class Meta:
        model = MediaFile
        fields = ['id', 'file', 'title', 'timestamp']

    def get_file_path(self, obj):
        url = self.context.get('request').scheme + '://' + self.context.get('request').get_host() + obj.file.url
        return url


class BoardContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'name', 'description']


class ColumnContentSerializer(serializers.ModelSerializer):
    deadline = serializers.DateTimeField()
    member = MemberDetialSerializer(many=True)

    class Meta:
        model = Column
        fields = ['id', 'name', 'description', 'deadline', 'order_position', 'member']


class GoalContentSerializer(serializers.ModelSerializer):
    deadline = serializers.DateTimeField()
    labels = LabelContentSerializer(many=True)
    member = MemberDetialSerializer(many=True)
    file = FileSerializer()

    class Meta:
        model = Goal
        fields = ['id', 'title', 'description', 'deadline', 'order_position', 'duration_hrs', 'priority', 'status',
                  'is_public', 'labels', 'member', 'file']


class ProjectDetailSerializer(serializers.ModelSerializer):
    member = MemberDetialSerializer(many=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'member', 'created_at']


class ProjectUpdateSerializer(WritableNestedModelSerializer):
    member = MemberSerializer(many=True)

    class Meta:
        model = Project
        fields = ['name', 'description', 'member']


class ProjectListSerializer(serializers.ModelSerializer):
    member = UserSerializer(many=True)
    user = UserSerializer()

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'member', 'user', 'member']
