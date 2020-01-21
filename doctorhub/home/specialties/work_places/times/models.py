from django.core.exceptions import ValidationError

from ..models import *


@register_snippet
class WeekDayIcon(SquareIcon):
    pass


SUNDAY = translation.pgettext_lazy('Week Day', 'Sunday')
MONDAY = translation.pgettext_lazy('Week Day', 'Monday')
TUESDAY = translation.pgettext_lazy('Week Day', 'Tuesday')
WEDNESDAY = translation.pgettext_lazy('Week Day', 'Wednesday')
THURSDAY = translation.pgettext_lazy('Week Day', 'Thursday')
FRIDAY = translation.pgettext_lazy('Week Day', 'Friday')
SATURDAY = translation.pgettext_lazy('Week Day', 'Saturday')

WEEK_DAY_CHOICES = [
    ('SUN', SUNDAY),
    ('MON', MONDAY),
    ('TUS', TUESDAY),
    ('WED', WEDNESDAY),
    ('THU', THURSDAY),
    ('FRI', FRIDAY),
    ('SAT', SATURDAY),
]


class WeekDay(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(WorkPlace, on_delete=models.CASCADE)
    day = models.CharField(
        max_length=3,
        choices=WEEK_DAY_CHOICES,
    )

    @staticmethod
    def get_default_icon():
        return WeekDayIcon.objects.first()

    @property
    def name(self):
        for char, day in WEEK_DAY_CHOICES:
            if char == self.day:
                return day

    class Meta:
        unique_together = [
            'owner', 'place', 'day'
        ]


class WorkTime(models.Model):
    day = models.ForeignKey(WeekDay, on_delete=models.CASCADE)
    begin = models.TimeField()
    end = models.TimeField()
