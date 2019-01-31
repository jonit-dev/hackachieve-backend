from django.views.decorators.csrf import csrf_exempt

from apps.boards.models import Board
from apps.columns.models import Column
from apps.columns_goals.models import Column_goal
from apps.goals.models import Goal
from apps.goals_categories.models import Goal_category
from apps.users_goals_categories.models import User_Goal_Category
from hackachieve.classes.Validator import *
from hackachieve.classes.API import *

# for protected views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny


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

    if User_Goal_Category.check_category_exists(json_data['category_name'], user.id) is True:
        return API.error_category_already_exists()

    category = User_Goal_Category(
        category_name=json_data['category_name'],
        user=user
    )
    category.save()

    return API.json_response({
        "status": "success",
        "message": "Your new category was created successfully!",
        "type": "success"
    })


@csrf_exempt
@api_view(['delete'])
@permission_classes((IsAuthenticated,))
def delete(request, category_id):
    user = User.objects.get(pk=API.getUserByToken(request))

    try:
        category = User_Goal_Category.objects.get(id=category_id, user_id=user.id)
    except Exception as e:  # and more generic exception handling on bottom
        return API.json_response({
            "status": "error",
            "message": "Error while trying to delete your category",
            "type": "error"
        })

    c = category.delete()

    if c:
        return API.json_response({
            "status": "success",
            "message": "Your category was deleted!",
            "type": "success"
        })


@csrf_exempt
@api_view(['post'])
@permission_classes((IsAuthenticated,))
def attach(request):
    json_data = API.json_get_data(request)

    user = User.objects.get(pk=API.getUserByToken(request))

    try:
        category = User_Goal_Category.objects.get(pk=json_data['category_id'])
        goal = Goal.objects.get(pk=json_data['goal_id'])
    except Exception as e:
        return API.json_response({
            "status": "error",
            "message": "Error while trying to attach your category",
            "type": "error"
        })

    print("Attaching category '{}' to goal '{}'".format(goal.title, category.category_name))

    # check if goal already has this category

    gc = Goal_category.objects.filter(goal=json_data['goal_id'], category=json_data['category_id']).exists()

    if gc is True:
        return API.json_response({
            "status": "error",
            "message": "This goal is already attached to this category",
            "type": "error"
        })

    Goal_category.attach(goal, category)

    return API.json_response({
        "status": "success",
        "message": "Goal {} attached to category {}".format(goal.id, category.id),
        "type": "success"
    })
