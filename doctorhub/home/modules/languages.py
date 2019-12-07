from django.shortcuts import get_object_or_404
from django.conf import settings

from ..multilingual.models import *


def get_language():
    language_code = translation.get_language()
    return get_object_or_404(Language, language_code=language_code)


def get_all_languages():
    return Language.objects.all()


def get_default_language():
    return get_object_or_404(
        Language, language_code=settings.LANGUAGE_CODE
    )


