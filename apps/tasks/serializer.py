from rest_framework import serializers

from apps.checklists.models import Checklist
from apps.goals.models import Goal
from apps.projects.models import Project
from apps.tasks.models import Task


class TaskCreateSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    deadline = serializers.DateTimeField(input_formats=['%Y-%M-%d'])
    checklist = serializers.PrimaryKeyRelatedField(queryset=Checklist.objects.all())

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'project', 'deadline', 'checklist']


class TaskUpdateSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    deadline = serializers.DateTimeField(input_formats=['%Y-%M-%d'])
    checklist = serializers.PrimaryKeyRelatedField(queryset=Checklist.objects.all())

    class Meta:
        model = Task
        fields = ['title', 'description', 'project', 'deadline', 'checklist', 'completed', 'priority']


class GoalDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'


class CheckListSerializer(serializers.ModelSerializer):
    goal = GoalDetailSerializer()

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
