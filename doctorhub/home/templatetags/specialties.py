from django import template

from ..modules import specialties

register = template.Library()


@register.simple_tag
def get_specialties(user):
    return specialties.get_user_specialties(user)


@register.simple_tag
def is_specialist(user):
    return specialties.is_specialist(user)

