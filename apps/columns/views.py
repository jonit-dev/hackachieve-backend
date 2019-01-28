from django.shortcuts import render
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


# Create your views here.
@csrf_exempt
@api_view(['post'])
@permission_classes((IsAuthenticated,))
def create(request):
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

        user = User.objects.get(pk=int(json_data['user_id']))

    except Exception as e:

        return API.json_response({
            "status": "error",
            "message": "This user does not exists",
            "type": "danger"
        })

    # check if user already has a board with the same name

    check_board = Board.objects.filter(name=json_data['name'], user_id=json_data['user_id'])

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