from django.shortcuts import get_object_or_404

from ..models import *


def get_home_page():
    return DigitalTebPageMixin.get_home_page()


def get_blogs_page():
    return DigitalTebPageMixin.get_blogs_page()


def get_specialists_page():
    return DigitalTebPageMixin.get_specialists_page()


def get_medical_centers_page():
    return DigitalTebPageMixin.get_medical_centers_page()


def get_specialist_page(user):
    return get_object_or_404(SpecialistPage, user=user)


def get_work_place_page(place):
    return get_object_or_404(WorkPlacePage, place=place)


def get_specialty_page(specialty):
    return get_object_or_404(SpecialtyPage, specialty=specialty)


def get_medical_center_page(medical_center):
    return get_object_or_404(MedicalCenterPage, medical_center=medical_center)


def create_specialist_page(user):
    parent = DigitalTebPageMixin.get_specialists_page()
    page = SpecialistPage(user=user)
    create_page(parent, page)


def create_page(parent_page, new_page):
    parent_page.add_child(instance=new_page)
    new_page.save()
