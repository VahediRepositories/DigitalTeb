from ..models import *
from ..modules import pages


def get_notifications(user):
    notifications = []
    for notification in user.notifications.all().unread():
        if notification.verb == ArticlePageComment.NEW_COMMENT:
            notifications.append(
                {
                    'sender': notification.actor.profile,
                    'title': translation.gettext('New Comment!'),
                    'description': translation.gettext(
                        '%(somebody)s commented on your post.'
                    ) % {'somebody': notification.actor.profile.name},
                    'url': notification.target.get_url(),
                }
            )
        elif notification.verb == ArticlePageComment.COMMENT_REPLY:
            notifications.append(
                {
                    'sender': notification.actor.profile,
                    'title': translation.gettext('Comment Reply!'),
                    'description': translation.gettext(
                        '%(somebody)s replied to your comment.'
                    ) % {'somebody': notification.actor.profile.name},
                    'url': notification.target.get_url(),
                }
            )
        elif notification.verb == Membership.MEMBERSHIP_REQUEST:
            notifications.append(
                {
                    'sender': notification.actor.profile,
                    'title': translation.gettext('Membership Request!'),
                    'description': translation.gettext(
                        '%(somebody)s sent a membership request for %(somewhere)s.'
                    ) % {'somebody': notification.actor.profile.name, 'somewhere': notification.target.name},
                    'url': reverse(
                        'work_place_profile', kwargs={
                            'pk': notification.target.pk
                        }
                    )
                }
            )
        elif notification.verb == Membership.MEMBERSHIP_ACCEPTED:
            notifications.append(
                {
                    'sender': notification.actor.profile,
                    'title': translation.gettext('Membership Request Accepted!'),
                    'description': translation.gettext(
                        '%(somebody)s accepted your membership request for %(somewhere)s.'
                    ) % {'somebody': notification.actor.profile.name, 'somewhere': notification.target.name},
                    'url': reverse(
                        'work_place_profile', kwargs={
                            'pk': notification.target.pk
                        }
                    )
                }
            )
        elif notification.verb == Membership.MEMBERSHIP_REJECTED:
            notifications.append(
                {
                    'sender': notification.actor.profile,
                    'title': translation.gettext('Membership Request Rejected!'),
                    'description': translation.gettext(
                        '%(somebody)s rejected your membership request for %(somewhere)s.'
                    ) % {'somebody': notification.actor.profile.name, 'somewhere': notification.target.name},
                    'url': pages.get_work_place_page(notification.target).get_url()
                }
            )
        elif notification.verb == Membership.MEMBERSHIP_CANCELED:
            notifications.append(
                {
                    'sender': notification.actor.profile,
                    'title': translation.gettext('Membership Canceled!'),
                    'description': translation.gettext(
                        "%(somebody)s's membership at %(somewhere)s was canceled."
                    ) % {'somebody': notification.actor.profile.name, 'somewhere': notification.target.name},
                    'url': reverse(
                        'work_place_profile', kwargs={
                            'pk': notification.target.pk
                        }
                    )
                }
            )
    return notifications
