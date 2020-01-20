from django.shortcuts import get_object_or_404

from ...specialties.work_places.phones.models import *
from ...specialties.work_places.images.models import *
from ...specialties.work_places.equipments.models import *
from .. import images
from .. import text_processing


def save_place_image(place, image_data):
    try:
        file_name = f'{place.name}'

        def save_image(file_path, content_file):
            place.image.save(
                file_path, content_file, save=True
            )

        images.save_base64_to_file(file_name, image_data, save_image)
    except Exception as e:
        import traceback
        traceback.print_exc()


def get_place_phones(place):
    return WorkPlacePhone.objects.filter(place=place)


def get_place_equipments(place):
    return Equipment.objects.filter(place=place)


def get_place_images(place):
    return WorkPlaceImage.objects.filter(place=place)


def get_user_work_places(user):
    return WorkPlace.objects.filter(owner=user)


def get_user_active_cities(user):
    cities = []
    for place in get_user_work_places(user):
        if place.city not in cities:
            cities.append(place.city)
    return cities


def get_user_active_cities_str(user):
    cities = get_user_active_cities(user)
    return text_processing.str_list_to_comma_separated(
        [
            city.name for city in cities
        ]
    )


def is_in_city(user, city):
    city = get_object_or_404(City, name=city)
    return city in get_user_active_cities(user)
