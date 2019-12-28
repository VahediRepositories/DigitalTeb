from django.conf import settings
from django.contrib.auth.models import Group, User
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db import models
from django.forms import TextInput
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldRowPanel, FieldPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from ..modules import images
from ..multilingual.mixins import *


class SpecialtyManager(models.Manager):
    def search(self, **kwargs):
        qs = self.get_queryset()
        if kwargs.get('name', ''):
            name_query = Q(name__icontains=kwargs['name'])
            specialist_name_query = Q(specialist_name__icontains=kwargs['name'])
            qs = qs.filter(
                name_query | specialist_name_query
            )
        return qs


@register_snippet
class Specialty(MultilingualModelMixin, models.Model):
    name = models.TextField()
    specialist_name = models.TextField(default='')
    group = models.OneToOneField(
        Group, on_delete=models.SET_NULL, blank=False, null=True
    )

    panels = [
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
                        FieldPanel(f'specialist_name_{language}', widget=TextInput)
                        for language in languages.get_all_translated_field_postfixes()
                    ]
                ),
            ], heading='Specialist Name', classname="collapsible collapsed"
        ),
        MultiFieldPanel(
            [
                FieldPanel('group')
            ], heading='Group', classname="collapsible collapsed"
        )
    ]

    @property
    def default_name(self):
        current = translation.get_language()
        translation.activate(settings.LANGUAGE_CODE)
        name = self.name
        translation.activate(current)
        return name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Specialties"

    def save(self, *args, **kwargs):
        self.set_multilingual_fields(
            ['name', 'specialist_name']
        )
        super().save(*args, **kwargs)

    objects = SpecialtyManager()


class LabelManager(models.Manager):

    def search(self, **kwargs):
        qs = self.get_queryset()
        if kwargs.get('name', ''):
            name_query = Q(name__icontains=kwargs['name'])
            description_query = Q(description__icontains=kwargs['name'])
            qs = qs.filter(
                name_query | description_query
            )
        return qs


@register_snippet
class Label(MultilingualModelMixin, models.Model):
    # TODO: change user to owner
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=500, blank=True)

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

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.set_multilingual_fields(
            ['name', 'description']
        )
        super().save(*args, **kwargs)

    objects = LabelManager()


@register_snippet
class Biography(MultilingualModelMixin, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=False)
    biography = models.TextField()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Biographies'

    def save(self, *args, **kwargs):
        self.set_multilingual_fields(
            ['biography']
        )
        super().save(*args, **kwargs)


@register_snippet
class Education(MultilingualModelMixin, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.CharField(max_length=200)
    field = models.CharField(max_length=500)
    institution = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        self.set_multilingual_fields(
            ['level', 'field', 'institution']
        )
        super().save(*args, **kwargs)


@register_snippet
class MedicalCenter(MultilingualModelMixin, models.Model):
    name = models.CharField(max_length=100)
    plural_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    panels = [
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


PLACES = 'doctorhub/more/images/places/'
HOSPITAL_ICON = PLACES + 'hospital.png'


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
                owner__first_name__icontains=kwargs['name']
            ) | Q(
                owner__last_name__icontains=kwargs['name']
            )
            name_query = Q(name__icontains=kwargs['name'])
            address_query = Q(address__icontains=kwargs['name'])
            qs = qs.filter(
                medical_center_query | city_query | owner_query | name_query | address_query
            )
        return qs


@register_snippet
class WorkPlace(MultilingualModelMixin, models.Model):
    medical_center = models.ForeignKey(
        MedicalCenter, on_delete=models.SET_NULL, blank=True, null=True,
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
            return static(HOSPITAL_ICON)

    panels = [
        SnippetChooserPanel('medical_center'),
        SnippetChooserPanel('city'),
        FieldPanel('owner'),
        FieldPanel('name'),
        FieldPanel('website'),
        FieldPanel('address'),
        FieldPanel('logo_image'),
    ]

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
