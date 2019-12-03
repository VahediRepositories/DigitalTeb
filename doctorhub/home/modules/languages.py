from django.shortcuts import get_object_or_404

from ..multilingual.models import *


def get_language():
    language_code = translation.get_language()
    return get_object_or_404(Language, language_code=language_code)


def get_all_languages():
    return Language.objects.all()


