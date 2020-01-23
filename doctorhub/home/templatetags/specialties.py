from django import template

from ..accounts.models import *

register = template.Library()


@register.simple_tag
def get_specialties(user):
    return specialties.get_user_specialties(user)


@register.simple_tag
def is_specialist(user):
    return specialties.is_specialist(user)


@register.simple_tag
def specialists_size():
    return len(Profile.specialists.all())


@register.simple_tag
def all_specialties():
    return specialties.get_all_specialties()


@register.simple_tag
def specialty_size(specialty):
    return len(specialties.get_specialist_users(specialty))
