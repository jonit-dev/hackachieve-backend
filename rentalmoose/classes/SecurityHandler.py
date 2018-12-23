import json
import requests

from rentalmoose.classes.API import *
from rentalmoose.classes.Environment import *


class SecurityHandler:
    allowed_regions = ["CA"]

    @staticmethod
    def prepare_phone_number(phone):
        phone = phone.replace("(", "").replace(")", "").replace(" ", "").replace("-", "")
        return phone

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    @staticmethod
    def check_regions(required_region_code, required_country, data):

        if required_region_code is None:
            if required_country == data['country_code']:
                return True
            else:
                return False
        else:
            if required_country == data['country_code'] and required_region_code == data['region_code']:
                return True
            else:
                return False

    @staticmethod
    def is_allowed_ip(ip, required_country="CA", required_region_code=None):
        env = Environment.getkey('env')
        IPSTACK_KEY = Environment.getkey('ipstack')

        if env == 'prod':
            response = requests.get("http://api.ipstack.com/{}?access_key={}&format=1".format(ip, IPSTACK_KEY))
            json_data = json.loads(response.text)
            return SecurityHandler.check_regions(required_region_code, required_country, json_data)



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

            print("{} => {}".format(response['country_code'], required_country))
            return SecurityHandler.check_regions(required_region_code, required_country, response)

    @staticmethod
    def is_allowed_phone(phone, area_code, country_code):
        env = Environment.getkey('env')
        WHITEPAGES_KEY = Environment.getkey('whitepages')

        # scammers generally use VOIP based lines

        """
                  Landline: Traditional wired phone line
                  FixedVOIP: VOIP based fixed line phones
                  Mobile: Wireless phone line
                  Voicemail: Voicemail-only service
                  TollFree: Callee pays for call
                  Premium: Caller pays a premium for the call–e.g. 976 area code
                  NonFixedVOIP: Skype, for example
                  Other: Anything that does not match the previous categories
        """
        forbidden_line_types = ['VOIP', "Voicemail", "Premium", "FixedVOIP", "NonFixedVOIP"]

        def phone_check(data):
            if data['line_type'] in forbidden_line_types:
                print("line type flag")
                return False

            if len(data['current_addresses']) > 0:  # if we found some address
                if area_code != data['current_addresses'][0]['state_code']:
                    print("area code flag")
                    return False

                if country_code != data['current_addresses'][0]['country_code']:
                    print("country code flag")
                    return False
            else:
                return False

            if data['is_valid'] != True:
                print("invalid number flag")
                return False

            return True

        if env == 'prod':
            response = {
                "id": "Phone.29c76fef-a2e1-4b08-cfe3-bc7128b7a075",
                "phone_number": "7788467427",
                "is_valid": True,
                "country_calling_code": "1",
                "line_type": "Mobile",
                "carrier": "Bell Cellular",
                "is_prepaid": None,
                "is_commercial": None,
                "belongs_to": [],
                "current_addresses": [
                    {
                        "id": "Location.c2d26bbc-f1d3-4089-8bc9-f91e9a0a7ccd",
                        "location_type": "PostalCode",
                        "street_line_1": None,
                        "street_line_2": None,
                        "city": "Vancouver",
                        "postal_code": "V5Z 1C5",
                        "zip4": None,
                        "state_code": "BC",
                        "country_code": "CA",
                        "lat_long": {
                            "latitude": 49.2486,
                            "longitude": -123.1202,
                            "accuracy": "PostalCode"
                        },
                        "is_active": None,
                        "delivery_point": None,
                        "link_to_person_start_date": None
                    }
                ],
                "historical_addresses": [],
                "associated_people": [],
                "alternate_phones": [],
                "error": None,
                "warnings": []
            }

            return phone_check(response)

        if env == 'dev':
            response = requests.get(
                "https://proapi.whitepages.com/3.0/phone.json?api_key={}&phone={}".format(WHITEPAGES_KEY, phone))
            json_data = json.loads(response.text)

            return phone_check(json_data)
