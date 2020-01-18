from django.contrib.auth.models import User
from django.utils import translation

from ...images.mixins import SquareIconMixin
from ...images.models import SquareIcon
from ...locations.cities.models import *


@register_snippet
class MedicalCenter(SquareIcon, MultilingualModelMixin, models.Model):
    name = models.CharField(max_length=100)
    plural_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    panels = SquareIcon.panels + [
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel(f'name_{language}', widget=TextInput)
                        for language in languages.get_all_translated_field_postfixes()
                    ]
                ),
            ], heading='Name', classname="collapsible collapsed"
        ),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel(f'plural_name_{language}', widget=TextInput)
                        for language in languages.get_all_translated_field_postfixes()
                    ]
                ),
            ], heading='Plural Name', classname="collapsible collapsed"
        ),
    ]

    @property
    def default_plural_name(self):
        return self.get_default_field('plural_name')

    def save(self, *args, **kwargs):
        self.set_multilingual_fields(
            ['name', 'plural_name']
        )
        super().save(*args, **kwargs)


class WorkPlaceManager(models.Manager):

    def search(self, **kwargs):
        qs = self.get_queryset()
        if kwargs.get('name', ''):
            medical_center_query = languages.multilingual_field_search(
                'medical_center__name', kwargs['name']
            ) | languages.multilingual_field_search(
                'medical_center__plural_name', kwargs['name']
            )
            city_query = languages.multilingual_field_search(
                'city__name', kwargs['name']
            )
            owner_query = languages.multilingual_field_search(
                'owner__profile__first_name', kwargs['name']
            ) | languages.multilingual_field_search(
                'owner__profile__last_name', kwargs['name']
            )
            name_query = languages.multilingual_field_search('name', kwargs['name'])
            address_query = languages.multilingual_field_search(
                'address', kwargs['name']
            )
            equipment_query = languages.multilingual_field_search(
                'equipment__name', kwargs['name']
            ) | languages.multilingual_field_search(
                'equipment__description', kwargs['name']
            )
            qs = qs.filter(
                medical_center_query | city_query | owner_query | name_query | address_query | equipment_query
            )
        return qs


EAST = 'E'
WEST = 'W'
NORTH = 'N'
SOUTH = 'S'

REGION_CHOICES = [
    (EAST, translation.gettext_lazy('East')),
    (WEST, translation.gettext_lazy('West')),
    (NORTH, translation.gettext_lazy('North')),
    (SOUTH, translation.gettext_lazy('South'))
]


class WorkPlace(MultilingualModelMixin, SquareIconMixin, models.Model):
    medical_center = models.ForeignKey(
        MedicalCenter, on_delete=models.PROTECT, blank=False, null=True,
        verbose_name=translation.gettext_lazy('Medical Center'),
    )
    city = models.ForeignKey(City, on_delete=models.PROTECT, null=True, blank=False)
    region = models.CharField(
        max_length=1,
        choices=REGION_CHOICES,
        default=EAST,
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False)
    website = models.URLField(blank=True)
    address = models.CharField(max_length=400, blank=False)
    image = models.ImageField(
        upload_to='workplace_images', null=True, blank=True
    )

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        else:
            return self.medical_center.image_url

    def has_staff(self, user):
        return self.owner == user

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.set_multilingual_fields(
            ['name', 'address']
        )
        super().save(*args, **kwargs)
        self.make_square_image()
        self.compress_image()

    objects = WorkPlaceManager()
