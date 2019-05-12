import base64
import json
from django.http import HttpResponse
from django.core import serializers

from apps.cities.models import City
from apps.provinces.models import Province


class API:

    @staticmethod
    def getUserByToken(request):
        # find header and get token
        header = request.META.get('HTTP_AUTHORIZATION')

        jwt = header.split(" ")[1]
        token = jwt.split('.')[1]

        # # now identify user by token

        token = str.encode(token)
        # Solve missing padding bug
        missing_padding = len(token) % 4
        if missing_padding != 0:
            token += b'=' * (4 - missing_padding)

        user_data = base64.b64decode(token).decode('UTF-8')

        # print(user_data)
        user_data = user_data.replace('"', '')
        user_data = user_data.replace('{', '')
        user_data = user_data.replace('}', '')

        user_data = list(user_data.split(','))

        for data in user_data:
            if "user_id" in data:
                user_id = data.split(':')[1]
                return user_id

        return False

    @staticmethod
    def json_get_data(request):
        json_data = json.loads(request.body.decode('utf-8'))
        # print(json_data)

        return json_data

    @staticmethod
    def json_response(response):
        return HttpResponse(json.dumps(response), content_type="application/json")

    @staticmethod
    def clean_fields(data, additional_fields=None):
        final_results = []
        for d in json.loads(data):

            if additional_fields is not None:
                for af in additional_fields:
                    d['fields'][af['key']] = af['value']

            d['fields']['id'] = d['pk']
            del d['pk']
            del d['model']
            d = d['fields']
            final_results.append(d)

        return final_results

    @staticmethod
    def serialize_model(object):

        # This script is responsible for converting django models into JSON responses, to be sent out through our API

        data = serializers.serialize('json', object)
        final_results = []
        for d in json.loads(data):
            d['fields']['id'] = d['pk']
            del d['pk']
            del d['model']
            d = d['fields']
            final_results.append(d)

        return final_results

    @staticmethod
    def serialize_model_multiple(list):

        # This script is responsible for converting django models into JSON responses, to be sent out through our API
        final_results = []
        for object in list:
            data = serializers.serialize('json', object)

            for d in json.loads(data):
                d['fields']['id'] = d['pk']
                del d['pk']
                del d['model']
                d = d['fields']

                if 'province' in d:
                    province = Province.objects.get(pk=d['province'])

                    d['province_abbrev'] = province.abbrev
                    d['type'] = "city"
                if 'city' in d:
                    city = City.objects.get(pk=d['city'])
                    d['city_name'] = city.name
                    d['type'] = "neighborhood"

                final_results.append(d)

        return final_results

    @staticmethod
    def serialize_single_object(Model, id):
        data = serializers.serialize("json", Model.objects.filter(pk=id))
        final_results = []

        for d in json.loads(data):
            d['fields']['id'] = d['pk']
            del d['pk']
            del d['model']
            d = d['fields']
            final_results.append(d)

        return final_results

    # ================================================================= #
    #                      ERROR MESSAGES
    # ================================================================= #

    @staticmethod
    def error_goal_user_is_not_owner():
        return API.json_response({
            "status": "error",
            "message": "This user is not allowed to access this goal",
            "type": "danger"
        })


    @staticmethod
    def error_goal_already_exists():
        return API.json_response({
            "status": "error",
            "message": "Goal with the same title already exists",
            "type": "danger"
        })

    @staticmethod
    def error_goal_not_found():
        return API.json_response({
            "status": "error",
            "message": "Goal not found.",
            "type": "danger"
        })

    @staticmethod
    def error_goal_inexistent_column():
        return API.json_response({
            "status": "error",
            "message": "Trying to add goal to inexistent column",
            "type": "danger"
        })

    @staticmethod
    def error_user_doesnt_exists():
        return API.json_response({
            "status": "error",
            "message": "This user does not exists",
            "type": "danger"
        })

    @staticmethod
    def error_board_not_found():
        return API.json_response({
            "status": "error",
            "message": "Board not found",
            "type": "error"
        })

    @staticmethod
    def error_user_already_has_this_board():
        return API.json_response({
            "status": "error",
            "message": "This user already has this board",
            "type": "danger"
        })

    @staticmethod
    def error_category_already_exists():
        return API.json_response({
            "status": "error",
            "message": "This category already exists",
            "type": "danger"
        })
