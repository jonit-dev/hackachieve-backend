import datetime

from datetime import *

from django.views.decorators.csrf import csrf_exempt

from apps.boards.models import Board
from apps.columns.models import Column
from apps.goals.models import Goal
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
    today = datetime.strptime(datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d')

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
        duration_hrs=0,
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
    today = datetime.strptime(datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d')

    if today > short_term_deadline:
        return API.json_response({
            "status": "error",
            "message": "Your cannot schedule a goal to a date before today ({})".format(today.date()),
            "type": "danger"
        })

    # updating =========================== #

    try:
        goal = Goal.objects.filter(id=goal_id, user_id=user.id).update(**json_data)
    except Exception as e:  # and more generic exception handling on bottom
        return API.json_response({
            "status": "error",
            "message": "Error while trying to update your goal",
            "type": "error"
        })

    if goal:
        return API.json_response({
            "status": "success",
            "message": "Your goal was updated!",
            "type": "success"
        })


@csrf_exempt
@api_view(['delete'])
@permission_classes((IsAuthenticated,))
def delete(request, goal_id):
    user = User.objects.get(pk=API.getUserByToken(request))

    try:
        goal = Goal.objects.get(id=goal_id, user_id=user.id)
    except Exception as e:  # and more generic exception handling on bottom
        return API.json_response({
            "status": "error",
            "message": "Error while trying to delete the goal",
            "type": "error"
        })

    c = goal.delete()

    if c:
        return API.json_response({
            "status": "success",
            "message": "Your goal was deleted!",
            "type": "success"
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

    goal_dict = model_to_dict(goal)

    return JsonResponse(goal_dict, safe=False)


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

    goal_dict = model_to_dict(goal)

    return JsonResponse(goal_dict, safe=False)


@csrf_exempt
@api_view(['get'])
@permission_classes((IsAuthenticated,))
def show(request, goal_id):
    user = User.objects.get(pk=API.getUserByToken(request))

    if Goal.check_goal_by_id(user.id, goal_id) is False:
        return API.error_goal_not_found()

    goal = Goal.objects.get(pk=goal_id)

    goal_dict = model_to_dict(goal)

    return JsonResponse(goal_dict, safe=False)


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
