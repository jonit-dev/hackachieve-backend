from django.views.decorators.csrf import csrf_exempt
from apps.boards.models import Board
from apps.projects.models import Project
from hackachieve.classes.BoardHandler import BoardHandler
from hackachieve.classes.Validator import *
from hackachieve.classes.API import *

# for protected views
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import JsonResponse


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

    user = User.objects.get(pk=API.getUserByToken(request))

    # check if user already has a board with the same name

    if Board.check_user_has_board(user.id, json_data['name']) is True:
        return API.error_user_already_has_this_board()

    obj = Project.objects.filter(id=json_data['project'])
    if len(obj) == 0:
        raise serializers.ValidationError("Project ID " + str(json_data['project']) + " does not exist in database")

    if obj[0].user.id != request.user.id:
        raise serializers.ValidationError(
            "Current User does not have permission to create board with project ID " + str(json_data['project']))

    board = Board(
        name=json_data['name'],
        user=user,
        description=json_data['description'],
        project_id=json_data['project']
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
def show_board(request, board_id, goal_type):
    user = User.objects.get(pk=API.getUserByToken(request))

    if int(board_id) == 0:  # get all boards information

        boards = Board.objects.filter(user_id=user.id)  # get all boards that I own

        boards_info = []

        for board in boards:
            board_columns_goals = BoardHandler.get_columns_and_goals(board, goal_type)

            boards_info.append(board_columns_goals)

        return JsonResponse(boards_info, safe=False)

    else:
        if Board.check_board_exists(board_id) is False:
            return API.error_board_not_found()

        board = Board.objects.get(id=board_id, user_id=user.id)

        board_columns_goals = BoardHandler.get_columns_and_goals(board, goal_type)

        return JsonResponse(board_columns_goals, safe=False)


@csrf_exempt
@api_view(['delete'])
@permission_classes((IsAuthenticated,))
def delete_board(request, board_id):
    user = User.objects.get(pk=API.getUserByToken(request))

    # Check board exists
    if Board.check_board_exists(board_id) is False:
        return API.error_board_not_found()

    board = Board.objects.get(id=board_id, user_id=user.id)
    b = board.delete()

    if b:
        return API.json_response({
            "status": "success",
            "message": "Your board was deleted!",
            "type": "success"
        })
