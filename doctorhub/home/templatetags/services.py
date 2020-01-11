from django import template

from ..specialties.services.models import *
from ..modules.specialties import services

register = template.Library()


@register.simple_tag
def service_default_image_url():
    return Label.get_default_icon().image_url


@register.simple_tag
def user_services(user):
    return services.get_user_services(user)


@register.simple_tag
def user_services_str(user):
    return services.get_user_services_str(user)
