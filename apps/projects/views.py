# Create your views here.
from rest_framework import mixins, viewsets, status, serializers
from rest_framework.response import Response

from apps.boards.models import Board
from apps.boards.serializer import LongTermSerializer, ShortTermSerializer, BoardListSerializer, GoalCommentSerializer
from apps.columns.models import Column
from apps.goals.models import Goal, GoalComment
from apps.projects.models import Project
from apps.projects.serializer import ProjectCreateSerializer, ProjectDetailSerializer, ProjectUpdateSerializer, \
    MemberSerializer, ProjectListSerializer
from apps.users.models import User
from django.db.models import Q


class ProjectViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """  Project ViewSet  """

    queryset = Project.objects.all()
    serializer_class = ProjectCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProjectDetailSerializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            if instance.user == request.user:
                self.perform_destroy(instance)
                return Response({'status': 'success', 'message': 'Record Deleted Successfully'},
                                status=status.HTTP_200_OK)
            else:
                return Response({'status': 'fail', 'message': 'You have not permission to delete this record '},
                                status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.user.id != request.user.id:
            raise serializers.ValidationError("You do not have permission to update Project")

        userlist = request.data.get('member')
        for user in userlist:
            valid_user = User.objects.filter(id=user['id'])
            if len(valid_user) != 1:
                raise serializers.ValidationError("Member user must have valid ID")

        serializer = ProjectUpdateSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        if instance.user == request.user:
            self.perform_update(serializer)
            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        else:
            return Response({'status': 'fail', 'message': 'You have not permission to update this record '},
                            status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        result = []
        queryset = Project.objects.filter(Q(member=request.user.id) | Q(user=request.user.id))
        serializer = ProjectListSerializer(queryset, many=True)
        projects = serializer.data
        for project in projects:
            board_result = []
            boards = Board.objects.filter(project=project['id'])
            board_result = self.get_board_list(boards)
            for index, board in enumerate(board_result):
                long_term = Column.objects.filter(board=board['id']).order_by('order_position')
                columns = self.get_long_term_goal(long_term)
                board_result[index]['long_term_goal'] = columns
                for index2, column in enumerate(columns):
                    goal = Goal.objects.filter(column=column['id']).order_by('order_position')
                    goals = self.get_short_term_goal(goal)
                    board_result[index]['long_term_goal'][index2]['short_term_goal'] = goals
                    for index3, item in enumerate(goals):
                        comment = GoalComment.objects.filter(goal=item['id']).order_by('id')
                        comments = self.get_goal_comment(comment)
                        board_result[index]['long_term_goal'][index2]['short_term_goal'][index3]['comments'] = comments

            project['board'] = board_result
            result.append(project)

        return Response(result)

    @staticmethod
    def get_board_list(queryset):
        boards = []
        for board in queryset:
            board_serializer = BoardListSerializer(board)
            boards.append(board_serializer.data)
        return boards

    @staticmethod
    def get_long_term_goal(queryset):
        columns = []
        for column in queryset:
            board_serializer = LongTermSerializer(column)
            columns.append(board_serializer.data)
        return columns

    @staticmethod
    def get_short_term_goal(queryset):
        goals = []
        for goal in queryset:
            board_serializer = ShortTermSerializer(goal)
            goals.append(board_serializer.data)
        return goals

    @staticmethod
    def get_goal_comment(queryset):
        comments = []
        for comment in queryset:
            comment_serializer = GoalCommentSerializer(comment)
            comments.append(comment_serializer.data)
        return comments

