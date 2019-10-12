from django import template
from ..modules import text_processing

register = template.Library()


@register.filter(name='html_to_str')
def html_to_str(html):
    return text_processing.html_to_str(html)


@register.filter(name='replace_white_space_with_underscore')
def replace_white_space_with_underscore(s):
    return s.replace(' ', '_')
