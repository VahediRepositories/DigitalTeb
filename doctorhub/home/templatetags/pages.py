from django import template

from ..modules import list_processing, pages, authentication

register = template.Library()


@register.simple_tag
def home_page_url():
    return pages.get_home_page().get_url()


@register.simple_tag
def blogs_url():
    return pages.get_blogs_page().get_url()


@register.simple_tag
def specialists_url():
    return pages.get_specialists_page().get_url()


@register.simple_tag
def medical_centers_url():
    return pages.get_medical_centers_page().get_url()


@register.simple_tag
def specialist_url(user):
    return pages.get_specialist_page(user).get_url()


@register.simple_tag
def profile_url(user):
    return authentication.get_profile_url(user)


@register.simple_tag
def profile_edit_url(user):
    return authentication.get_profile_edit_url(user)


@register.simple_tag
def specialty_page_url(specialty):
    return pages.get_specialty_page(specialty).get_url()


@register.simple_tag
def medical_center_page_url(medical_center):
    return pages.get_medical_center_page(medical_center).get_url()


@register.simple_tag
def in_rows(objects, row_size):
    return list_processing.list_to_sublists_of_size_n(objects, row_size)


@register.simple_tag
def articles_category_url(category):
    return pages.get_articles_category_page(category).get_url()
