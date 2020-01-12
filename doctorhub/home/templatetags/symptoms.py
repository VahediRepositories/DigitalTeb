from django import template

from ..specialties.symptoms.models import *

register = template.Library()


@register.simple_tag
def symptom_default_image_url():
    return Symptom.get_default_icon().image_url
