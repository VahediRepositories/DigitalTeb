from django import template

from ..specialties.education.models import *
from ..modules.specialties import education

register = template.Library()


@register.simple_tag
def education_default_image_url():
    return Education.get_default_icon().image_url


@register.simple_tag
def user_education_records(user):
    return education.get_user_education_records(user)
