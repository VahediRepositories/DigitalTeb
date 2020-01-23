from django import template

from ..modules import articles

register = template.Library()


@register.simple_tag
def all_categories():
    return articles.get_all_categories()
