from django import template

from ..models import DigitalTebPageMixin

register = template.Library()


@register.simple_tag
def home_page_url():
    return DigitalTebPageMixin.get_home_page().get_url()


@register.simple_tag
def blogs_url():
    return DigitalTebPageMixin.get_blogs_page().get_url()

