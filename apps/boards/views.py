from django.views.decorators.csrf import csrf_exempt

from apps.boards.models import Board
from apps.boards_goals.models import Board_goal
from apps.goals.models import Goal
from apps.goals_categories.models import Goal_category
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

    user = User.objects.get(pk=API.getUserByToken(request))

    # check if user already has a board with the same name

    if Board.check_user_has_board(user.id, json_data['name']) is True:
        return API.error_user_already_has_this_board()

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

    if Board.check_board_exists(board_id) is False:
        return API.error_board_not_found()

    board = Board.objects.get(id=board_id, user_id=user.id)

    board_dict = model_to_dict(board)

    return JsonResponse(board_dict, safe=False)


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


@csrf_exempt
@api_view(['post'])
@permission_classes((IsAuthenticated,))
def attach_to_goal(request):
    json_data = API.json_get_data(request)
    user = User.objects.get(pk=API.getUserByToken(request))

    if not Board.check_board_exists(json_data['board_id']):
        return API.error_board_not_found()

    if not Goal.check_goal_by_id(user.id, json_data['goal_id']):
        return API.error_goal_not_found()

    board = Board.objects.get(pk=json_data['board_id'])
    goal = Goal.objects.get(pk=json_data['goal_id'])

    if Board_goal.objects.filter(board=json_data['board_id'], goal=json_data['goal_id']).exists() is True:
        return API.json_response({
            "status": "error",
            "message": "This board already has this associated goal",
            "type": "error"
        })

    else:

        Board_goal.attach(board, goal)

        return API.json_response({
            "status": "success",
            "message": "Your goal was successfully attached to the board",
            "type": "success"
        })


@csrf_exempt
@api_view(['get'])
@permission_classes((IsAuthenticated,))
def show_goals(request, board_id):
    user = User.objects.get(pk=API.getUserByToken(request))

    if Board.check_board_exists(board_id) is False:
        return API.error_board_not_found()

    goals = Board_goal.objects.get(board=board_id).goal.all()


    #custom goals serialization

    data = serializers.serialize('json', goals)
    final_results = []
    for d in json.loads(data):
        d['fields']['id'] = d['pk']
        del d['pk']
        del d['model']
        d = d['fields']

        try:  # add custom category field to response
            d['categories'] = API.serialize_model(Goal_category.objects.get(goal=d['id']).category.all())
        except Exception as e:
            d['categories'] = []

        final_results.append(d)

    return API.json_response(final_results)
