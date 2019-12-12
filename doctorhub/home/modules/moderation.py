from django.contrib.auth.models import Group


def make_user_moderator(user):
    group = get_moderators_group()
    group.user_set.add(user)


def get_moderators_group():
    return Group.objects.get(name='Moderators')
