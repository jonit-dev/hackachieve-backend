import base64
import json
import os
import shutil

from django.core.files.base import ContentFile
from django.http import HttpResponse

from apps.properties.models import Property
from rentalmoose import settings


class PropertyHandler:

    @staticmethod
    def get_base64_img_data(request_data_image):

        format, imgstr = request_data_image.split(';base64,')
        ext = format.split('/')[-1]

        filename = "{}.{}".format("property_image", ext)

        data = ContentFile(base64.b64decode(imgstr), name=filename)  # You can save this as file instance.
        return {
            "data": data,
            "ext": ext
        }

    @staticmethod
    def save_property(request_data, owner, property_type, img_data):

        property = Property(
            owner=owner,
            status=request_data['status'],
            title=request_data['title'],
            sqft=request_data['sqft'],
            type=property_type,
            rental_value=request_data['rental_value'],
            utilities_included=request_data['utilities_included'],
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
            available_to_move_in_date=request_data['available_to_move_in_date'],
            open_view_start=request_data['open_view_start'],
            open_view_end=request_data['open_view_end'],
            upload=img_data['data']

        )
        property.save()

        return property

    @staticmethod
    def reallocate_uploaded_files(property, img_data):

        property_id = str(property.id)
        os.mkdir(os.path.join(settings.PROPERTIES_IMAGES_ROOT, property_id))

        # setup some variables to help we handle it
        newdir_path = settings.PROPERTIES_IMAGES_ROOT + "/" + property_id
        large_img = "property_image" + ".large." + img_data['ext']
        normal_img = "property_image" + "." + img_data['ext']
        thumbnail_img = "property_image" + ".thumbnail." + img_data['ext']
        large_img_path = settings.PROPERTIES_IMAGES_ROOT + "/" + large_img
        normal_img_path = settings.PROPERTIES_IMAGES_ROOT + "/" + normal_img
        thumbnail_img_path = settings.PROPERTIES_IMAGES_ROOT + "/" + thumbnail_img

        # wait until images are saved, and then move them
        import time

        # try to save it when those files are available in our server
        while True:
            time.sleep(0.2)
            if os.path.isfile(large_img_path) is True and os.path.isfile(normal_img_path) and os.path.isfile(
                    thumbnail_img_path):
                shutil.move(large_img_path, newdir_path + "/" + large_img)
                shutil.move(normal_img_path, newdir_path + "/" + normal_img)
                shutil.move(thumbnail_img_path, newdir_path + "/" + thumbnail_img)
                break

    @staticmethod
    def check_file_extensions(ext):

        allowed_extensions = ["png", "jpeg", "bmp", "jpg"]

        if ext in allowed_extensions:
            return True
        else:
            return False
