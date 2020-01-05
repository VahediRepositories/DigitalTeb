from django import template

from .. import configurations

register = template.Library()


@register.simple_tag
def search_limit():
    return configurations.SEARCH_LIMIT
