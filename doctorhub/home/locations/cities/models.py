from django.db import models
from django.forms import TextInput
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldRowPanel, FieldPanel
from wagtail.snippets.models import register_snippet

from ...multilingual.mixins import *


class CityManager(models.Manager):

    def search(self, **kwargs):
        qs = self.get_queryset()
        if kwargs.get('name', ''):
            qs = qs.filter(
                languages.multilingual_field_search('name', kwargs['name'])
            )
        return qs


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

    @property
    def default_name(self):
        return self.get_default_field('name')

    class Meta:
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.set_multilingual_fields(
            ['name']
        )
        super().save(*args, **kwargs)

    objects = CityManager()

    class Meta:
        ordering = ['id']
