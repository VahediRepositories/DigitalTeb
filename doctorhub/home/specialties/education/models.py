from django.contrib.auth.models import User
from django.db import models
from wagtail.snippets.models import register_snippet

from ...multilingual.mixins import MultilingualModelMixin
from ...images.models import SquareIcon


@register_snippet
class EducationIcon(SquareIcon):
    pass


@register_snippet
class Education(MultilingualModelMixin, models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.CharField(max_length=200)
    field = models.CharField(max_length=500)
    institution = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        self.set_multilingual_fields(
            ['level', 'field', 'institution']
        )
        super().save(*args, **kwargs)

    @property
    def image_url(self):
        return self.get_default_icon().image_url

    @staticmethod
    def get_default_icon():
        return EducationIcon.objects.last()
