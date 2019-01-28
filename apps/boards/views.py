from django.views.decorators.csrf import csrf_exempt

from apps.boards.models import Board
from hackachieve.classes.Validator import *
from hackachieve.classes.API import *

# for protected views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

import json
from django.core import serializers

from django.http import JsonResponse
from django.forms.models import model_to_dict


@csrf_exempt
@api_view(['post'])
@permission_classes((IsAuthenticated,))
def create_board(request):
    json_data = API.json_get_data(request)


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

        user = User.objects.get(pk=API.getUserByToken(request))

    except Exception as e:

        return API.json_response({
            "status": "error",
            "message": "This user does not exists",
            "type": "danger"
        })

    # check if user already has a board with the same name

    check_board = Board.objects.filter(name=json_data['name'], user_id=user.id)

    if len(check_board) >= 1:
        return API.json_response({
            "status": "error",
            "message": "This board already exists",
            "type": "danger"
        })

    board = Board(
        name=json_data['name'],
        type=json_data['type'],
        user=user
    )
    board.save()

    return API.json_response({
        "status": "success",
        "message": "Your new board was created successfully!",
        "type": "success"
    })


@csrf_exempt
@api_view(['get'])
@permission_classes((IsAuthenticated,))
def show_all_boards(request):
    user = User.objects.get(pk=API.getUserByToken(request))

    # fetch only your own boards
    boards = Board.objects.filter(user_id=user.id)

    return API.json_response(API.serialize_model(boards))


@csrf_exempt
@api_view(['get'])
@permission_classes((IsAuthenticated,))
def show_board(request, board_id):
    from django.core import serializers
    user = User.objects.get(pk=API.getUserByToken(request))
    board = Board.objects.get(id=board_id, user_id=user.id)

    board_dict = model_to_dict(board)

    return JsonResponse(board_dict, safe=False)


@csrf_exempt
@api_view(['delete'])
@permission_classes((IsAuthenticated,))
def delete_board(request, board_id):
    user = User.objects.get(pk=API.getUserByToken(request))

    try:
        board = Board.objects.get(id=board_id, user_id=user.id)
    except Exception as e:  # and more generic exception handling on bottom
        return API.json_response({
            "status": "error",
            "message": "Error while trying to delete the board",
            "type": "error"
        })

    b = board.delete()

    if b:
        return API.json_response({
            "status": "success",
            "message": "Your board was deleted!",
            "type": "success"
        })
