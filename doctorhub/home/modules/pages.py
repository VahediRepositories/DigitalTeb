from ..models import *


def create_specialist_page(user):
    parent = DigitalTebPageMixin.get_specialists_page()
    page = SpecialistPage(user=user)
    parent.add_child(instance=page)
    page.save()
