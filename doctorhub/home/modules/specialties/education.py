from ...specialties.education.models import *


def get_user_education_records(user):
    return Education.objects.filter(owner=user)
