from django import template

from ..modules import notifications

register = template.Library()


@register.simple_tag
def user_notifications(user):
    return notifications.get_notifications(user)
