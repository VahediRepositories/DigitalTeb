from django import template

from ..modules.specialties import work_places

register = template.Library()


@register.simple_tag
def work_place_default_image_url():
    return work_places.get_default_work_place().image_url


@register.simple_tag
def place_phones(place):
    return work_places.get_place_phones(place)
