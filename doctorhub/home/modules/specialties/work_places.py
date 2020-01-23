from django.db.models import Q
from django.shortcuts import get_object_or_404

from ...specialties.work_places.phones.models import *
from ...specialties.work_places.images.models import *
from ...specialties.work_places.times.models import *
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
    places = [
        place for place in WorkPlace.objects.filter(owner=user)
    ]
    employments = Membership.objects.filter(employee=user, status=Membership.ACCEPTED)
    for employment in employments:
        place = employment.place
        if place not in places:
            places.append(place)
    return places


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


def get_user_working_days(place, user):
    return WeekDay.objects.filter(place=place, owner=user)


def get_working_intervals(day):
    return WorkTime.objects.filter(day=day)


def is_working_time_valid(work_time):
    if work_time.begin >= work_time.end:
        return False
    for interval in WorkTime.objects.filter(day=work_time.day):
        if work_time.begin == interval.begin and work_time.end == interval.end:
            return False
        if work_time.begin >= interval.begin:
            if work_time.begin < interval.end:
                return False
        if interval.begin >= work_time.begin:
            if interval.begin < work_time.end:
                return False
    return True


def get_all_medical_centers():
    return MedicalCenter.objects.all()


def get_all_work_places(medical_center):
    return WorkPlace.objects.filter(medical_center=medical_center)
