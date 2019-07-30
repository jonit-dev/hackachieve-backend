from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from apps.checklists.models import Checklist
from apps.goals.models import Goal
from apps.projects.models import Project
from apps.projects.serializer import GoalContentSerializer
from apps.tasks.models import Task


class ChecklistTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checklist
        fields = ['id']


class TaskCreateSerializer(WritableNestedModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    deadline = serializers.DateTimeField(input_formats=['%Y-%M-%d'])
    checklist = ChecklistTaskSerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'project', 'deadline', 'checklist']


class TaskUpdateSerializer(WritableNestedModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    deadline = serializers.DateTimeField(input_formats=['%Y-%M-%d'])
    checklist = ChecklistTaskSerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = ['title', 'description', 'project', 'deadline', 'checklist', 'completed', 'priority']


class GoalDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'


class CheckListSerializer(serializers.ModelSerializer):
    goal = GoalContentSerializer()

    class Meta:
        model = Checklist
        fields = '__all__'


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class TaskDetailSerializer(serializers.ModelSerializer):
    checklist = CheckListSerializer()
    project = ProjectListSerializer()

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'project', 'deadline', 'checklist', 'completed', 'priority']


class TaskDetailForProjectSerializer(serializers.ModelSerializer):
    checklist = CheckListSerializer()

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'deadline', 'checklist', 'completed', 'priority']


class ProjectTaskDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description']
