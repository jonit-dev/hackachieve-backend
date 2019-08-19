from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import mixins, viewsets, status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response

from apps.boards.models import Board
from apps.columns.models import Column
from apps.columns.serializer import ColumnOrderSerializer, ColumnMemberCreateSerializer, ColumnMemberDetailSerializer, \
    ColumnSerializer
from apps.projects.models import Project
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
            "message": "Error while trying to create your board. The following fields are empty: {}".format(
                check_user_fields),
            "type": "danger"
        })

        # if all fields are set to create our board


    if not 'deadline' in json_data:
        return API.json_response({
            "status": "error",
            "message": "Please, select a long-term goal deadline.",
            "type": "danger"
        })

    try:
        user = User.objects.get(pk=user.id)

    except Exception as e:

        return API.json_response({
            "status": "error",
            "message": "This user does not exists",
            "type": "danger"
        })

    # check if board exists

    board_id = json_data['board_id']

    board_exists = Board.objects.filter(id=json_data['board_id']).exists()
    if not board_exists:

        # set category as default

        default_category = Board.objects.filter(user=request.user, name="Other")

        # if user didnt set a category for this new column, lets create one
        if not default_category.exists():
            # create one
            other_board = Board(name="Other", project=Project.objects.get(pk=json_data['project_id']),
                                user=request.user)
            other_board.save()
            board_id = other_board.id
        else:
            # if user alredy has "Other" board category

            board_id = default_category.first().id

    # check if theres a column with the same name for this user

    check_column = Column.objects.filter(user_id=user.id, name=json_data['name'])

    if len(check_column) >= 1:
        return API.json_response({
            "status": "error",
            "message": "Column with the same name already exists, for this user",
            "type": "danger"
        })

    # if not, create it

    new_column = Column(
        name=json_data['name'],
        board=Board.objects.get(pk=board_id),
        user=user,
        deadline=json_data['deadline']
    )

    if 'description' in json_data.keys():
        new_column.description = json_data['description']

    new_column.save()
    serializer = ColumnSerializer(new_column)
    return API.json_response({
        "status": "success",
        "message": "Your new main goal was created successfully!",
        "type": "success",
        "response": serializer.data
    })


@csrf_exempt
@api_view(['put'])
@permission_classes((IsAuthenticated,))
def update(request, column_id):
    json_data = API.json_get_data(request)
    user = User.objects.get(pk=API.getUserByToken(request))
    # Empty fields valitation =========================== #
    check_user_fields = Validator.are_request_fields_valid(json_data)

    # Check is theres no empty fields
    if check_user_fields is not True:
        return API.json_response({
            "status": "error",
            "message": "Error while trying to create your board. The following fields are empty: {}".format(
                check_user_fields),
            "type": "danger"
        })

        # if all fields are set to create our board

    try:
        user = User.objects.get(pk=user.id)

    except Exception as e:

        return API.json_response({
            "status": "error",
            "message": "This user does not exists",
            "type": "danger"
        })

    # check if column exists
    if Column.check_exists(column_id) is False:
        return API.error_goal_inexistent_column()

    # get column instance

    column = Column.objects.get(pk=column_id)

    column.name = json_data['name']
    column.description = json_data['description']
    column.board = Board.objects.get(pk=json_data['board_id'])
    column.deadline = json_data['deadline']

    column.save()

    return API.json_response({
        "status": "success",
        "message": "Your new column was updated successfully!",
        "type": "success"
    })


@csrf_exempt
@api_view(['post'])
@permission_classes((IsAuthenticated,))
def attach_category(request, column_id):
    json_data = API.json_get_data(request)
    user = User.objects.get(pk=API.getUserByToken(request))
    category = User_Category.objects.get(id=json_data['category_id'])

    # first we get the column
    column = Column.objects.get(id=column_id, user_id=user.id)

    # set relationship
    # Column_category.attach(column, category)

    return JsonResponse({
        "status": "success",
        "message": "Your category was attached to the column!",
        "type": "success"
    })


@csrf_exempt
@api_view(['get'])
@permission_classes((IsAuthenticated,))
def show_columns_from_board(request, board_id):
    user = User.objects.get(pk=API.getUserByToken(request))

    columns = Column.objects.filter(board_id=board_id, user_id=user.id)

    return API.json_response(API.serialize_model(columns))


@csrf_exempt
@api_view(['delete'])
@permission_classes((IsAuthenticated,))
def delete(request, column_id):
    user = User.objects.get(pk=API.getUserByToken(request))

    try:
        column = Column.objects.get(id=column_id, user_id=user.id)
    except Exception as e:  # and more generic exception handling on bottom
        return API.json_response({
            "status": "error",
            "message": "Error while trying to delete the column",
            "type": "error"
        })

    c = column.delete()

    if c:
        return API.json_response({
            "status": "success",
            "message": "Your column was deleted!",
            "type": "success"
        })


class UpdateColumnViewSets(GenericAPIView, UpdateModelMixin):
    '''   we update Column order position '''
    queryset = Column.objects.all()
    serializer_class = ColumnOrderSerializer

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class GoalMemberViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """  Goal Member ViewSet  """

    queryset = Column.objects.all()
    serializer_class = ColumnMemberCreateSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ColumnMemberDetailSerializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        userlist = request.data.get('member')
        for user in userlist:
            valid_user = User.objects.filter(id=user['id'])
            if len(valid_user) != 1:
                return Response({
                    "status": "error",
                    "message": "Member user must have valid ID",
                    "type": "error"
                },
                    status=status.HTTP_200_OK)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        if instance.user == request.user:
            self.perform_update(serializer)
            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
            return Response(serializer.data)
        else:
            return Response(
                {"status": "error",
                 "message": "You have not permission to update this record ",
                 "type": "danger"
                 },
                status=status.HTTP_200_OK)
