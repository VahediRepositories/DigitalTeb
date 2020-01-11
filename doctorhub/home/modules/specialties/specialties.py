from django.http import Http404

from ...specialties.models import *


def make_user_specialist(user, specialty_default_name):
    specialty = get_specialty_by_default_name(specialty_default_name)
    specialty.group.user_set.add(user)
    group = get_specialists_group()
    group.user_set.add(user)


def get_specialty_by_default_name(default_name):
    for specialty in Specialty.objects.all():
        if specialty.default_name == default_name:
            return specialty
    raise Http404


def get_specialists_group():
    return Group.objects.get(name='Specialists')


def is_specialist(user):
    return user.groups.filter(
        name=get_specialists_group().name
    ).exists()


def get_all_specialties():
    return Specialty.objects.all()


def get_user_specialties(user):
    specialties = []
    for specialty in get_all_specialties():
        group = specialty.group
        if user.groups.filter(
            name=group.name
        ).exists():
            specialties.append(specialty)
    return specialties
