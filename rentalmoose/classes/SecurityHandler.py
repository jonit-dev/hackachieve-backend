import json
import requests

from rentalmoose.classes.API import *
from rentalmoose.classes.Environment import *


class SecurityHandler:

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    @staticmethod
    def is_allowed_ip(ip, required_country, required_region_code):
        env = Environment.getkey('env')
        IPSTACK_KEY = Environment.getkey('ipstack')

        response = requests.get("http://api.ipstack.com/{}?access_key={}&format=1".format(ip, IPSTACK_KEY))
        json_data = json.loads(response.text)

        if env == 'prod':

            if json_data["country_code"] is not required_country:
                return False
            elif json_data["region_code"] is not required_region_code:
                return False

            return True
        else: #on dev, always return true
            return True
