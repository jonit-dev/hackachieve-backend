import json
from django.http import HttpResponse


class API:

    @staticmethod
    def json_get_data(request):
        json_data = json.loads(request.body.decode('utf-8'))
        print(json_data)

        return json_data

    @staticmethod
    def json_response(response):
        return HttpResponse(json.dumps(response), content_type="application/json")
