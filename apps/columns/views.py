from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from apps.boards.models import Board
from apps.columns.models import Column
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

    try:
        user = User.objects.get(pk=user.id)

    except Exception as e:

        return API.json_response({
            "status": "error",
            "message": "This user does not exists",
            "type": "danger"
        })

    # check if board exists
    check_board = Board.objects.filter(id=json_data['board_id'])
    if len(check_board) is 0:
        return API.json_response({
            "status": "error",
            "message": "Trying to add column to inexistent board",
            "type": "danger"
        })

    # check if theres a column with the same name for this user

    check_column = Column.objects.filter(user_id=user.id, name=json_data['name'])

    if len(check_column) > 1:
        return API.json_response({
            "status": "error",
            "message": "Column with the same name already exists, for this user",
            "type": "danger"
        })

    # if not, create it

    new_column = Column(
        name=json_data['name'],
        board=Board.objects.get(pk=json_data['board_id']),
        user=user
    )
    new_column.save()

    return API.json_response({
        "status": "success",
        "message": "Your new column was created successfully!",
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
