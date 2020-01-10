from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.forms import TextInput
from django.utils import translation
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldRowPanel, FieldPanel
from wagtail.snippets.models import register_snippet

from ...images.models import SquareIcon
from ...multilingual.mixins import MultilingualModelMixin
from ...modules import languages, images


@register_snippet
class City(MultilingualModelMixin, models.Model):
    name = models.CharField(max_length=50)

    panels = [
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel(f'name_{language}', widget=TextInput)
                        for language in languages.get_all_translated_field_postfixes()
                    ]
                ),
            ], heading='Name', classname="collapsible"
        )
    ]

    class Meta:
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.set_multilingual_fields(
            ['name']
        )
        super().save(*args, **kwargs)


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

    def save(self, *args, **kwargs):
        self.set_multilingual_fields(
            ['name', 'plural_name']
        )
        super().save(*args, **kwargs)


class WorkPlaceManager(models.Manager):

    def search(self, **kwargs):
        qs = self.get_queryset()
        if kwargs.get('name', ''):
            medical_center_query = Q(
                medical_center__name=kwargs['name']
            ) | Q(
                medical_center__plural_name=kwargs['name']
            )
            city_query = Q(city__name__icontains=kwargs['name'])
            owner_query = Q(
                owner__profile__first_name__icontains=kwargs['name']
            ) | Q(
                owner__profile__last_name__icontains=kwargs['name']
            )
            name_query = Q(name__icontains=kwargs['name'])
            address_query = Q(address__icontains=kwargs['name'])
            qs = qs.filter(
                medical_center_query | city_query | owner_query | name_query | address_query
            )
        return qs


class WorkPlace(MultilingualModelMixin, models.Model):
    medical_center = models.ForeignKey(
        MedicalCenter, on_delete=models.SET_NULL, blank=False, null=True,
        verbose_name=translation.gettext_lazy('Medical Center'),
    )
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False)
    website = models.URLField(blank=True)
    address = models.CharField(max_length=400, blank=False)
    logo_image = models.ImageField(
        upload_to='workplace_images', null=True, blank=True
    )

    @property
    def image_url(self):
        if self.logo_image:
            return self.logo_image.url
        else:
            return self.medical_center.image_url

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.set_multilingual_fields(
            ['name', 'address']
        )
        super().save(*args, **kwargs)
        self.make_square_image()
        self.compress_image()

    def make_square_image(self):
        if self.logo_image:
            images.make_square_image(self.logo_image.path)

    def compress_image(self):
        if self.logo_image:
            images.compress_image(self.logo_image.path)

    objects = WorkPlaceManager()


@register_snippet
class WorkPlacePhone(models.Model):
    place = models.ForeignKey(WorkPlace, on_delete=models.CASCADE)
    phone = models.CharField(max_length=30)
