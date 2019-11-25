from django.contrib.auth.models import User
from django.db import models
from django.db.models import DateField
from wagtail.snippets.models import register_snippet

MALE = 'M'
FEMALE = 'F'
NOT_BINARY = 'N'

GENDER_CHOICES = [
    (NOT_BINARY, 'هيچكدام'),
    (FEMALE, 'زن'),
    (MALE, 'مرد'),
]


@register_snippet
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ForeignKey(
        'wagtailimages.Image',
        help_text='high quality image',
        null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default=NOT_BINARY,
    )
    birthdate = DateField(blank=False)

    def __str__(self):
        return self.user.username
