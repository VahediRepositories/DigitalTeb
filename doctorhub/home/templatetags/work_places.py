from django import template
from django.shortcuts import get_object_or_404

from ..modules.specialties import work_places
from ..specialties.work_places.models import *

register = template.Library()


@register.simple_tag
def work_place_default_image_url():
    return WorkPlace.get_default_icon().image_url


@register.simple_tag
def place_phones(place):
    return work_places.get_place_phones(place)


@register.simple_tag
def place_images(place):
    return work_places.get_place_images(place)


@register.simple_tag
def place_equipments(place):
    return work_places.get_place_equipments(place)


@register.simple_tag
def active_cities(user):
    return work_places.get_user_active_cities(user)


@register.simple_tag
def user_working_days(place, user):
    return work_places.get_user_working_days(place, user)


@register.simple_tag
def working_intervals(day):
    return work_places.get_working_intervals(day)


@register.simple_tag
def all_medical_centers():
    return work_places.get_all_medical_centers()


@register.simple_tag
def medical_centers_size():
    return len(WorkPlace.objects.all())


@register.simple_tag
def medical_center_size(medical_center):
    return len(work_places.get_all_work_places(medical_center))


@register.simple_tag
def user_work_places(user):
    return work_places.get_user_work_places(user)


@register.simple_tag
def employment(user, place):
    return get_object_or_404(
        Membership, employee=user, place=place, status=Membership.ACCEPTED
    )

