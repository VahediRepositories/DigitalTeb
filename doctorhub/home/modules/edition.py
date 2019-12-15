from django.contrib.auth.models import Group


def make_user_editor(user):
    group = get_editors_group()
    group.user_set.add(user)


def get_editors_group():
    return Group.objects.get(name='Editors')
