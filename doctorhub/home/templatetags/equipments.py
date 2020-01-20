from django import template

from ..specialties.work_places.equipments.models import *
from ..modules.specialties import equipments

register = template.Library()


@register.simple_tag
def equipment_default_image_url():
    return Equipment.get_default_icon().image_url


@register.simple_tag
def place_equipments_str(place):
    return equipments.get_place_equipments_str(place)
