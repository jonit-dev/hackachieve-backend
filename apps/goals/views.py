import datetime

from datetime import *

from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status, mixins
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.response import Response

from apps.boards.models import Board
from apps.columns.models import Column
from apps.goals.models import Goal, GoalComment, CommentVote
from apps.goals.serializer import (
    GoalSerializer,
    GoalPublicStatusSerializer,
    GoalCommentSerializer,
    GoalCommentDetailSerializer,
    CommentVoteSerializer,
    GoalCommentUpdateSerializer, GoalCommentCreateSerializer)
from apps.goals.models import Goal
from apps.goals.serializer import GoalSerializer, GoalPublicStatusSerializer, GoalOrderSerializer
from hackachieve.classes.Validator import *
from hackachieve.classes.API import *

# for protected views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

import json
from django.core import serializers

from django.http import JsonResponse
from django.forms.models import model_to_dict


# Create your views here.
@csrf_exempt
@api_view(['post'])
@permission_classes((IsAuthenticated,))
def create(request):
    json_data = API.json_get_data(request)

    user = User.objects.get(pk=API.getUserByToken(request))

    # Empty fields valitation =========================== #
    check_user_fields = Validator.are_request_fields_valid(json_data)

    # Check is theres no empty fields
    if check_user_fields is not True:
        return API.json_response({
            "status": "error",
            "message": "Error while trying to create your goal. The following fields are empty: {}".format(
                check_user_fields),
            "type": "danger"
        })

    # if all fields are set to create our board

    if User.check_user_exists(user.id) is False:
        return API.error_user_doesnt_exists()

    # check if column exists
    if Column.check_exists(json_data['column_id']) is False:
        return API.error_goal_inexistent_column()

    # check if theres a column with the same name for this user

    if Goal.check_goal_by_title(user.id, json_data['title']) is True:
        return API.error_goal_already_exists()

    # check if short term goal deadline > long term goal deadline

    short_term_deadline = datetime.strptime(json_data['deadline'], '%Y-%m-%d')
    long_term_deadline = datetime.strptime(Column.objects.get(pk=json_data['column_id']).deadline.strftime('%Y-%m-%d'),
                                           '%Y-%m-%d')

    if short_term_deadline > long_term_deadline:
        return API.json_response({
            "status": "error",
            "message": "Your short-term goal deadline ({}) must be before your long-term goal deadline ({})".format(
                short_term_deadline.date(), long_term_deadline.date()),
            "type": "danger"
        })

    # check if user is trying to schedule a goal to the past
    today = datetime.strptime(
        datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d')

    if today > short_term_deadline:
        return API.json_response({
            "status": "error",
            "message": "Your cannot schedule a goal to a date before today ({})".format(today.date()),
            "type": "danger"
        })

    # create new datetime
    date = json_data['deadline'].split('-')

    # # if not, create it
    new_goal = Goal(
        user=User.objects.get(pk=user.id),
        title=json_data['title'],
        description=json_data['description'],
        duration_hrs=int(json_data['optional_duration_hrs']
                         ) if json_data['optional_duration_hrs'] else 0,
        deadline=datetime(int(date[0]), int(date[1]), int(date[2])),
        column=Column.objects.get(pk=json_data['column_id']),
        priority=json_data['priority'],
        status=1  # always active on creation
    )
    new_goal.save()

    return API.json_response({
        "status": "success",
        "message": "Your new goal was created successfully!",
        "type": "success"
    })


@csrf_exempt
@api_view(['put', 'patch'])
@permission_classes((IsAuthenticated,))
def update(request, goal_id):
    user = User.objects.get(pk=API.getUserByToken(request))
    json_data = API.json_get_data(request)

    # validation =========================== #

    short_term_deadline = datetime.strptime(json_data['deadline'], '%Y-%m-%d')
    long_term_deadline = datetime.strptime(Column.objects.get(pk=json_data['column_id']).deadline.strftime('%Y-%m-%d'),
                                           '%Y-%m-%d')

    if short_term_deadline > long_term_deadline:
        return API.json_response({
            "status": "error",
            "message": "Your short-term goal deadline ({}) must be before your long-term goal deadline ({})".format(
                short_term_deadline.date(), long_term_deadline.date()),
            "type": "danger"
        })

    # check if user is trying to schedule a goal to the past
    today = datetime.strptime(
        datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d')

    if today > short_term_deadline:
        return API.json_response({
            "status": "error",
            "message": "Your cannot schedule a goal to a date before today ({})".format(today.date()),
            "type": "danger"
        })

    goal = Goal.objects.get(pk=goal_id)

    if goal.user.id is not user.id:
        return API.json_response({
            "status": "error",
            "message": "You cannot update a goal that is not yours.",
            "type": "error"
        })

    # updating =========================== #

    try:
        goal = Goal.objects.filter(
            id=goal_id, user_id=user.id).update(**json_data)
        return API.json_response({
            "status": "success",
            "message": "Your goal was updated successfully!",
            "type": "success"
        })

    except Exception as e:  # and more generic exception handling on bottom
        return API.json_response({
            "status": "error",
            "message": "Error while trying to update your goal",
            "type": "error"
        })


@csrf_exempt
@api_view(['delete'])
@permission_classes((IsAuthenticated,))
def delete(request, goal_id):
    user = User.objects.get(pk=API.getUserByToken(request))

    try:
        goal = Goal.objects.get(id=goal_id, user_id=user.id)

        goal.delete()

        return API.json_response({
            "status": "success",
            "message": "Your goal was deleted!",
            "type": "success"
        })
    except Exception as e:  # and more generic exception handling on bottom
        return API.json_response({
            "status": "error",
            "message": "Error while trying to delete the goal",
            "type": "error"
        })


@csrf_exempt
@api_view(['post'])
@permission_classes((IsAuthenticated,))
def attach_to_column(request):
    json_data = API.json_get_data(request)
    user = User.objects.get(pk=API.getUserByToken(request))

    # check if column exists
    if Column.check_exists(json_data['column_id']) is False:
        return API.error_goal_inexistent_column()

    column = Column.objects.get(pk=json_data['column_id'])
    goal = Goal.objects.get(pk=json_data['goal_id'])

    # if Column_goal.objects.filter(column=json_data['column_id'], goal=json_data['goal_id']).exists() is True:
    #     return API.json_response({
    #         "status": "error",
    #         "message": "This goal is already attached to this column".format(goal.id, column.id),
    #         "type": "error"
    #     })
    #
    # print("Attaching goal '{}' to column '{}'".format(goal.title, column.name))
    # Column_goal.attach(column, goal)

    return API.json_response({
        "status": "success",
        "message": "Goal {} attached to column {}".format(goal.id, column.id),
        "type": "success"
    })


@csrf_exempt
@api_view(['patch'])
@permission_classes((IsAuthenticated,))
def update_status(request, goal_id, status_id):
    user = User.objects.get(pk=API.getUserByToken(request))

    if Goal.check_user_owns_goal(user.id, goal_id) is False:
        return API.error_goal_user_is_not_owner()

    if Goal.check_goal_by_id(user.id, goal_id) is False:
        return API.error_goal_not_found()

    goal = Goal.objects.get(pk=goal_id)
    goal.status = int(status_id)

    goal.save()

    response = json.loads(serializers.serialize('json', [goal]))[0]['fields']

    return API.json_response(response)


@csrf_exempt
@api_view(['patch'])
@permission_classes((IsAuthenticated,))
def update_priority(request, goal_id, priority):
    user = User.objects.get(pk=API.getUserByToken(request))

    if Goal.check_user_owns_goal(user.id, goal_id) is False:
        return API.error_goal_user_is_not_owner()

    if Goal.check_goal_by_id(user.id, goal_id) is False:
        return API.error_goal_not_found()

    goal = Goal.objects.get(pk=goal_id)
    goal.priority = int(priority)

    goal.save()

    response = json.loads(serializers.serialize('json', [goal]))[0]['fields']

    return JsonResponse(response, safe=False)


@csrf_exempt
@api_view(['get'])
@permission_classes((IsAuthenticated,))
def show(request, goal_id):
    user = User.objects.get(pk=API.getUserByToken(request))

    if Goal.check_goal_by_id(user.id, goal_id) is False:
        return API.error_goal_not_found()

    goal = Goal.objects.get(pk=goal_id)

    serializer = GoalSerializer(goal)
    return Response(serializer.data)


@csrf_exempt
@api_view(['get'])
@permission_classes((IsAuthenticated,))
def long_short(request, long_term_goal_id):
    user = User.objects.get(pk=API.getUserByToken(request))

    if Goal.check_goal_by_id(user.id, long_term_goal_id) is False:
        return API.error_goal_not_found()

    goal = Goal.objects.get(pk=long_term_goal_id)

    goal_dict = model_to_dict(goal)

    return JsonResponse(goal_dict, safe=False)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class GoalFeedsViewSet(viewsets.ModelViewSet):
    """
    A Goal ViewSet for listing or retrieving users.
    """
    queryset = Goal.objects.filter(is_public=True).order_by('order_position')
    serializer_class = GoalSerializer
    pagination_class = StandardResultsSetPagination

    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PublicGoalUpdateView(GenericAPIView, UpdateModelMixin):
    '''
    we update Goal visibility Public or Private
    '''
    queryset = Goal.objects.all()
    serializer_class = GoalPublicStatusSerializer

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class CommentPublicGoal(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    ''' Comment Public Goal   '''

    queryset = GoalComment.objects.all()
    serializer_class = GoalCommentSerializer

    def list(self, request, *args, **kwargs):
        queryset = GoalComment.objects.none()
        if request.GET.get('goal', None):
            queryset = GoalComment.objects.filter(goal=request.GET['goal'])
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        if len(serializer.data) > 0:
            voting_response = self.get_vote_detail(serializer.data)
            return Response(voting_response)
        else:
            return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = GoalCommentCreateSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        item = request.data
        if self.check_public_goal(item['goal']):
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({'status': 'error', 'message': "Sorry, you're not allowed to comment on private goals."},
                            status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # check if the instance user is the same that's originating the request
        if instance.user.id != request.user.id:
            return Response({'status': 'error', 'message': "Sorry, you're not allowed to update a comment that is not yours."},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = GoalCommentUpdateSerializer(instance, data=request.data, context={
                                                    'request': request}, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = GoalCommentDetailSerializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.user.id != request.user.id:
            return Response({'status': 'error', 'message': "Sorry, you're not allowed to delete a comment that is not yours."},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            self.perform_destroy(instance)
        return Response({'status': 'success', 'message': 'Comment deleted successfully '},
                        status=status.HTTP_204_NO_CONTENT)

    def check_public_goal(self, id):
        """ check the goal is public or not """
        obj = Goal.objects.filter(is_public=True, id=id)
        if len(obj) > 0:
            return True
        else:
            return False

    def get_vote_detail(self, data):
        """ getting vote detail for each comment """
        resutl = []
        for item in data:
            item_dict = dict(item)
            obj = CommentVote.objects.filter(comment=item_dict['id'])
            if len(obj) > 0:
                upvote = obj.filter(upvote=1)
                downvote = obj.filter(downvote=1)
                vote = {'upvote': len(upvote), 'downvote': len(downvote)}
                item_dict['voting'] = [vote]
                resutl.append(item_dict)
            else:
                item_dict['voting'] = []
                resutl.append(item_dict)

        return resutl


class CommentVoteViewset(mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    """ Vote the Comment """

    queryset = CommentVote.objects.all()
    serializer_class = CommentVoteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        value = request.data
        if value['upvote'] != value['downvote']:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({'status': 'error', 'message': 'UP Vote and Down Vote must be different value'},
                            status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class OrderUpdateGoalView(GenericAPIView, UpdateModelMixin):
    '''   we update Goal order position '''
    queryset = Goal.objects.all()
    serializer_class = GoalOrderSerializer

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
