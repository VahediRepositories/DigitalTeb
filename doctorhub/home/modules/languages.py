from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.conf import settings

from ..multilingual.models import *


def get_language_codes():
    return [
        code for (code, lang) in settings.LANGUAGES
    ]


def get_language_code():
    language_codes = get_language_codes()
    language_code = translation.get_language()
    if language_code in language_codes:
        return language_code
    else:
        tokens = language_code.split('-')
        # if language code doesn't have sub-language code
        if len(tokens) == 1:
            for code in language_codes:
                if code.startswith(tokens[0]):
                    return code
        raise Http404


def get_language():
    language_code = get_language_code()
    return get_object_or_404(Language, language_code=language_code)


def get_all_languages():
    return Language.objects.all()


def get_default_language():
    return get_object_or_404(
        Language, language_code=settings.LANGUAGE_CODE
    )


def get_translated_field_postfix(language):
    return language.language_code.replace('-', '_')


def get_all_translated_field_postfixes():
    languages = get_all_languages()
    return [
        get_translated_field_postfix(language)
        for language in languages
    ]


def multilingual_field_search(field, value):
    query = Q()
    for postfix in get_all_translated_field_postfixes():
        kwargs = {
            f'{field}_{postfix}__icontains': value
        }
        query |= Q(**kwargs)
    return query
