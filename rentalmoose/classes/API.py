import base64
import json
from django.http import HttpResponse


class API:

    @staticmethod
    def getUserByToken(request):
        # find header and get token
        header = request.META.get('HTTP_AUTHORIZATION')
        jwt = header.split(" ")[1]
        token = jwt.split('.')[1]

        # print(token)

        # now identify user by token
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
