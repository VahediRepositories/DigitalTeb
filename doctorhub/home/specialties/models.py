from django.conf import settings
from django.contrib.auth.models import Group, User
from django.db import models
from django.forms import TextInput
from django.utils import translation
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldRowPanel, FieldPanel
from wagtail.snippets.models import register_snippet

from ..modules import languages


@register_snippet
class Specialty(models.Model):
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


@register_snippet
class Label(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.name


@register_snippet
class Biography(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=False)
    biography = models.TextField()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Biographies'


@register_snippet
class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.CharField(max_length=200)
    field = models.CharField(max_length=500)
    institution = models.CharField(max_length=200)


@register_snippet
class WorkPlace(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False)
    website = models.URLField()
    address = models.TextField()
    logo_image = models.ImageField(
        upload_to='logo_images', null=True, blank=True
    )

    def __str__(self):
        return self.name


@register_snippet
class WorkPlacePhone(models.Model):
    place = models.ForeignKey(WorkPlace, on_delete=models.CASCADE)
    phone = models.CharField(max_length=30)


@register_snippet
class MedicalCenter(models.Model):
    name = models.CharField(max_length=100)
    plural_name = models.CharField(max_length=100)
