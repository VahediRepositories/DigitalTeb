from django.shortcuts import get_object_or_404

from ..models import *


def get_home_page():
    return DigitalTebPageMixin.get_home_page()


def get_blogs_page():
    return DigitalTebPageMixin.get_blogs_page()


def get_specialists_page():
    return DigitalTebPageMixin.get_specialists_page()


def get_specialist_page(user):
    return get_object_or_404(SpecialistPage, user=user)


def create_specialist_page(user):
    parent = DigitalTebPageMixin.get_specialists_page()
    page = SpecialistPage(user=user)
    parent.add_child(instance=page)
    page.save()
