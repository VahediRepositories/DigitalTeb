from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db.models import DateField, Q
from django.utils import translation

from ..modules.specialties import specialties
from ..specialties.symptoms.models import *
from ..specialties.services.models import *
from ..specialties.work_places.models import *
from ..images.mixins import SquareIconMixin

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
        name = kwargs.get('name', '')
        city = kwargs.get('city', '')
        if city:
            qs = qs.filter(
                user__in=[
                    place.owner for place in WorkPlace.objects.filter(
                        city__in=[
                            City.objects.search(name=city)
                        ]
                    )
                ]
            )
        if name:
            first_name_query = languages.multilingual_field_search('first_name', name)
            last_name_query = languages.multilingual_field_search('last_name', name)
            symptom_query = Q(
                user__in=[
                    symptom.owner for symptom in Symptom.objects.search(name=name)
                ]
            )
            services_query = Q(
                user__in=[
                    service.owner for service in Label.objects.search(name=name)
                ]
            )
            qs = qs.filter(
                first_name_query | last_name_query | symptom_query | services_query
            )
        return qs


@register_snippet
class Profile(MultilingualModelMixin, SquareIconMixin, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=False, null=False, default='')
    last_name = models.CharField(max_length=50, blank=False, null=False, default='')
    image = models.ImageField(
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
        return f'{self.first_name} {self.last_name}'

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        else:
            if self.gender == MALE:
                return static(MALE_AVATAR)
            elif self.gender == FEMALE:
                return static(FEMALE_AVATAR)
            else:
                return static(NONE_AVATAR)

    def save(self, *args, **kwargs):
        self.set_multilingual_fields(
            ['first_name', 'last_name']
        )
        super().save(*args, **kwargs)
        self.make_square_image()
        self.compress_image()

    def __str__(self):
        return self.user.username


@register_snippet
class BirthDate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = DateField(blank=False, null=True)

    def __str__(self):
        return self.user.username
