from django.contrib.auth.models import User
from django.db import models
from django.utils import translation
from wagtail.snippets.models import register_snippet

from ...images.mixins import SquareIconMixin
from ...images.models import SquareIcon
from ...multilingual.mixins import *


@register_snippet
class SymptomIcon(SquareIcon):
    pass


class SymptomManager(models.Manager):

    def search(self, **kwargs):
        qs = self.get_queryset()
        if kwargs.get('name', ''):
            name_query = languages.multilingual_field_search('name', kwargs['name'])
            description_query = languages.multilingual_field_search('description', kwargs['name'])
            qs = qs.filter(
                name_query | description_query
            )
        return qs


class Symptom(MultilingualModelMixin, SquareIconMixin, models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(
        verbose_name=translation.gettext_lazy('Name'),
        max_length=100, blank=False
    )
    description = models.TextField(
        verbose_name=translation.gettext_lazy('Description'),
        blank=True
    )
    image = models.ImageField(
        upload_to='symptoms_images', null=True, blank=True
    )

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        else:
            return self.get_default_icon().image_url

    @staticmethod
    def get_default_icon():
        return SymptomIcon.objects.last()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.set_multilingual_fields(
            ['name', 'description']
        )
        super().save(*args, **kwargs)
        self.make_square_image()
        self.compress_image()

    objects = SymptomManager()
