from django import template

from ..models import *
from ..modules import list_processing, pages

register = template.Library()


@register.simple_tag
def home_page_url():
    return DigitalTebPageMixin.get_home_page().get_url()


@register.simple_tag
def blogs_url():
    return DigitalTebPageMixin.get_blogs_page().get_url()


@register.simple_tag
def specialists_url():
    return DigitalTebPageMixin.get_specialists_page().get_url()


@register.simple_tag
def specialist_url(user):
    return pages.get_specialist_page(user).get_url()


@register.simple_tag
def in_rows(objects, row_size):
    return list_processing.list_to_sublists_of_size_n(objects, row_size)
