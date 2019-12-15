from django.shortcuts import get_object_or_404

from ..models import *


def create_specialist_page(user):
    parent = DigitalTebPageMixin.get_specialists_page()
    page = SpecialistPage(user=user)
    parent.add_child(instance=page)
    page.save()


def get_specialist_page(user):
    return get_object_or_404(SpecialistPage, user=user)
