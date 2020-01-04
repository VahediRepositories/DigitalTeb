from django.contrib.auth.models import User
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db import models
from django.db.models import DateField, Q
from django.utils import translation
from wagtail.snippets.models import register_snippet

from ..modules import images
from ..modules import specialties

MALE = 'M'
FEMALE = 'F'
NOT_BINARY = 'N'

GENDER_CHOICES = [
    (
        NOT_BINARY,
        # Translators: This appears on registration page where users have to select their sex.
        translation.pgettext_lazy(
            'sex type', 'None of them'
        )
    ),
    (
        FEMALE,
        # Translators: This appears on registration page where users have to select their sex.
        translation.pgettext_lazy(
            'sex type', 'Female'
        )
    ),
    (
        MALE,
        # Translators: This appears on registration page where users have to select their sex.
        translation.pgettext_lazy(
            'sex type', 'Male'
        )
    ),
]

AVATARS = 'doctorhub/more/images/avatars/'
MALE_AVATAR = AVATARS + 'male.png'
FEMALE_AVATAR = AVATARS + 'female.png'
NONE_AVATAR = AVATARS + 'none.png'


class SpecialistsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            user__groups=specialties.get_specialists_group()
        )

    def search(self, **kwargs):
        qs = self.get_queryset()
        if kwargs.get('name', ''):
            first_name_query = Q(user__first_name__icontains=kwargs['name'])
            last_name_query = Q(user__last_name__icontains=kwargs['name'])
            qs = qs.filter(
                first_name_query | last_name_query
            )
        return qs


@register_snippet
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(
        upload_to='profile_pics', null=True, blank=True
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default=NOT_BINARY,
    )

    objects = models.Manager()
    specialists = SpecialistsManager()

    @property
    def name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @property
    def image_url(self):
        if self.profile_image:
            return self.profile_image.url
        else:
            if self.gender == MALE:
                return static(MALE_AVATAR)
            elif self.gender == FEMALE:
                return static(FEMALE_AVATAR)
            else:
                return static(NONE_AVATAR)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.make_square_image()
        self.compress_image()

    def make_square_image(self):
        if self.profile_image:
            images.make_square_image(self.profile_image.path)

    def compress_image(self):
        if self.profile_image:
            images.compress_image(self.profile_image.path)

    def __str__(self):
        return self.user.username


@register_snippet
class BirthDate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = DateField(blank=False, null=True)

    def __str__(self):
        return self.user.username
