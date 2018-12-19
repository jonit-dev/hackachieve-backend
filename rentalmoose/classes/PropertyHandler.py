import base64
import json
import os
import shutil

from django.core.files.base import ContentFile
from django.http import HttpResponse

from apps.properties.models import Property
from rentalmoose import settings
from rentalmoose.classes.API import API

from apps.cities.models import City
from apps.neighborhoods.models import Neighborhood



class PropertyHandler:

    @staticmethod
    def get_base64_img(base64imgdata):

        format, imgstr = base64imgdata.split(';base64,')
        # ext = format.split('/')[-1]
        ext = "jpeg"  # force jpeg extension
        filename = "{}.{}".format("property_image", ext)

        return {
            "base64data": base64.b64decode(imgstr),
            "ext": ext
        }

    @staticmethod
    def get_base64_img_data(request_data_image):

        format, imgstr = request_data_image.split(';base64,')
        # ext = format.split('/')[-1]
        ext = "jpeg"  # force jpeg extension

        filename = "{}.{}".format("property_image", ext)  # convert everything to JPEG

        data = ContentFile(base64.b64decode(imgstr), name=filename)  # You can save this as file instance.
        return {
            "data": data,
            "ext": ext
        }

    @staticmethod
    def save_property(request_data, owner, property_type):


        city = City.objects.get(pk=request_data['city']['id'])

        # Neighborhood is optional. Lets check if user passed it. If so, save. If not, set to None (null).
        if 'neighborhood' in request_data:
            neighborhood = Neighborhood.objects.get(pk=request_data['neighborhood']['id'])
        else:
            neighborhood = None


        #before saving, lets reformat dates

        move_in_date = request_data['available_to_move_in_date'].split("T")[0]
        open_view_start = request_data['open_view_start'].split("T")[0]
        open_view_end = request_data['open_view_end'].split("T")[0]

        property = Property(
            owner=owner,
            city=city,
            neighborhood=neighborhood,
            status=request_data['status'],
            title=request_data['title'],
            description=request_data['description'],
            sqft=request_data['sqft'],
            type=property_type,
            rental_value=request_data['rental_value'],
            utilities_included=request_data['utilities_included'],
            utilities_estimation=request_data['utilities_estimation'],
            n_bedrooms=request_data['n_bedrooms'],
            n_bathrooms=request_data['n_bathrooms'],
            address=request_data['address'],
            furnished=request_data['furnished'],
            no_pets=request_data['no_pets'],
            no_smoking=request_data['no_smoking'],
            no_parties=request_data['no_parties'],
            minimum_lease=request_data['minimum_lease'],
            pet_deposit=request_data['pet_deposit'],
            security_deposit=request_data['security_deposit'],
            publication_date=request_data['publication_date'],
            available_to_move_in_date=move_in_date,
            open_view_start=open_view_start,
            open_view_end=open_view_end,

        )
        property.save()

        return property

    @staticmethod
    def check_file_extensions(ext):

        allowed_extensions = ["png", "jpeg", "bmp", "jpg"]

        if ext in allowed_extensions:
            return True
        else:
            return False

    @staticmethod
    def is_owner(property, user):

        if property.owner_id != user.id:
            return False
        else:
            return True
