from django.views.decorators.csrf import csrf_exempt
from rentalmoose.classes.API import *
from rentalmoose.classes.Validator import *

# for protected views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


# CUSTOM VIEWS =========================== #

# ================================================================= #
#                      DASHBOARD
# ================================================================= #

# Protected view - dashboard
@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def user_dashboard(request):

    user_id = API.getUserByToken(request)

    return API.json_response({
        'content': "hi"
    })


# ================================================================= #
#                      REGISTER
# ================================================================= #

@csrf_exempt
def user_register(request):
    if request.method == "POST":

        # get json data

        json_data = API.json_get_data(request)

        # Empty fields valitation =========================== #

        check_user_fields = Validator.are_user_fields_valid(json_data)

        check_user_fields = Validator.are_user_fields_valid(json_data)

        if check_user_fields is not True:
            return API.json_response({
                "status": "error",
                "message": "Error while trying to create your account. The following fields are empty: {}".format(
                    ", ".join(check_user_fields)),
                "type": "danger"
            })
        elif not Validator.check_password_confirmation(json_data['password'], json_data['passwordConfirmation']):
            return API.json_response({
                "status": "error",
                "message": "Your password does not match its respective password confirmation. Please, try again.",
                "type": "danger"
            })
        elif Validator.check_user_exists(json_data['email']):
            return API.json_response({
                "status": "error",
                "message": "This e-mail is already registered in our system. Please, choose another one and try again.",
                "type": "danger"
            })

        else:  # if everything is ok, procceed

            # create user here

            create_user = User.objects.create_user(
                username=json_data['email'],
                email=json_data['email'],
                password=json_data['password'],
                first_name=json_data['firstName'],
                last_name=json_data['lastName'],
                type=1
            )

        if create_user:
            return API.json_response({
                "status": "success",
                "message": "Your account {} was created successfully! Redirecting...".format(json_data['email']),
                "type": "success"
            })
        else:
            return API.json_response({
                "status": "error",
                "message": "An error occured while trying to create your new user. Please, contact our support.",
                "type": "danger"
            })

    else:
        response = {
            "error": "Invalid request"
        }
    return HttpResponse(json.dumps(response), content_type="application/json")
