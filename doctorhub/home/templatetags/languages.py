from django import template

from ..modules import languages

register = template.Library()


@register.simple_tag
def get_active_language():
    return languages.get_language()


@register.simple_tag
def get_all_languages():
    return languages.get_all_languages()


@register.simple_tag
def get_current_url(request, language):
    return language.get_current_url(request)


@register.simple_tag
def is_rtl():
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    language = languages.get_language()
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@', language.direction, type(language.direction))
    return language.direction == languages.RTL


@register.simple_tag
def is_ltr():
    language = languages.get_language()
    return language.direction == languages.LTR
