from django import template

from ..specialties.work_places.equipments.models import *

register = template.Library()


@register.simple_tag
def equipment_default_image_url():
    return Equipment.get_default_icon().image_url
