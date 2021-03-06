from django.contrib.auth.models import Group
from django.db import models
from django.forms import TextInput
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldRowPanel, FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet

from ..multilingual.mixins import *


class SpecialtyManager(models.Manager):
    def search(self, **kwargs):
        qs = self.get_queryset()
        if kwargs.get('name', ''):
            name_query = languages.multilingual_field_search('name', kwargs['name'])
            specialist_name_query = languages.multilingual_field_search('specialist_name', kwargs['name'])
            qs = qs.filter(
                name_query | specialist_name_query
            )
        return qs


@register_snippet
class Specialty(MultilingualModelMixin, models.Model):
    name = models.TextField()
    specialist_name = models.TextField(default='')
    group = models.OneToOneField(
        Group, on_delete=models.PROTECT, blank=False, null=True
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        help_text='high quality square image',
        null=True, blank=False, on_delete=models.PROTECT, related_name='+'
    )

    panels = [
        MultiFieldPanel(
            [
                ImageChooserPanel('image')
            ], heading='Image', classname="collapsible collapsed"
        ),
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
        return self.get_default_field('name')

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
