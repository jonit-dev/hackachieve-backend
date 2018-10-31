import base64
import json
from django.http import HttpResponse
from django.core import serializers


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
        print(json_data)

        return json_data

    @staticmethod
    def json_response(response):
        return HttpResponse(json.dumps(response), content_type="application/json")

    @staticmethod
    def clean_fields(data):
        final_results = []
        for d in json.loads(data):
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
