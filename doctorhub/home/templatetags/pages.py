from django import template

from ..models import DigitalTebPageMixin
from ..modules import authentication

register = template.Library()


@register.simple_tag
def home_page_url():
    return DigitalTebPageMixin.get_home_page().get_url()


@register.simple_tag
def blogs_url():
    return DigitalTebPageMixin.get_blogs_page().get_url()


@register.simple_tag
def login_url():
    return authentication.get_login_url()


@register.simple_tag
def signup_url():
    return authentication.get_signup_url()


@register.simple_tag
def logout_url():
    return authentication.get_logout_url()
