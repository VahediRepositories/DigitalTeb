from django import template

from ..modules import specialties, text_processing

register = template.Library()


@register.simple_tag
def get_specialties(user):
    return specialties.get_user_specialties(user)


@register.simple_tag
def is_specialist(user):
    return specialties.is_specialist(user)


@register.simple_tag
def user_labels(user):
    return specialties.get_user_labels(user)


@register.simple_tag
def user_labels_str(user):
    labels = specialties.get_user_labels(user)
    return text_processing.str_list_to_comma_separated(
        [
            label.name for label in labels
        ]
    )


@register.simple_tag
def user_education_records(user):
    return specialties.get_user_education_records(user)
