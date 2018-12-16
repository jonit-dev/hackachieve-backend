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

        if env == 'prod':

            response = requests.get("http://api.ipstack.com/{}?access_key={}&format=1".format(ip, IPSTACK_KEY))
            json_data = json.loads(response.text)

            if required_country == json_data['country_code'] and required_region_code == json_data['region_code']:
                return True
            else:
                return False



        elif env == 'dev':  # on dev, always return true

            response = {
                "ip": "50.68.202.201",
                "type": "ipv4",
                "continent_code": "NA",
                "continent_name": "North America",
                "country_code": "CA",
                "country_name": "Canada",
                "region_code": "BC",
                "region_name": "British Columbia",
                "city": "North Vancouver",
                "zip": "V7N",
                "latitude": 49.35,
                "longitude": -123.0679,
                "location": {
                    "geoname_id": 6090785,
                    "capital": "Ottawa",
                    "languages": [
                        {
                            "code": "en",
                            "name": "English",
                            "native": "English"
                        },
                        {
                            "code": "fr",
                            "name": "French",
                            "native": "Français"
                        }
                    ],
                    "country_flag": "http://assets.ipstack.com/flags/ca.svg",
                    "country_flag_emoji": "🇨🇦",
                    "country_flag_emoji_unicode": "U+1F1E8 U+1F1E6",
                    "calling_code": "1",
                    "is_eu": False
                }
            }

            if required_country == response['country_code'] and required_region_code == response['region_code']:
                return True
            else:
                return False