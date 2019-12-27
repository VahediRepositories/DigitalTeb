from django.db import models
from django.urls import translate_url
from django.utils import translation
from wagtail.snippets.models import register_snippet

RTL = 'rtl'
LTR = 'ltr'

LANGUAGE_DIR_CHOICES = [
    (
        RTL,
        translation.gettext_lazy('right to left')
    ),
    (
        LTR,
        translation.gettext_lazy('left to right')
    ),
]


@register_snippet
class Language(models.Model):
    language_code = models.CharField(
        max_length=5,
        unique=True,
    )

    english_name = models.TextField()
    name = models.TextField()

    direction = models.CharField(
        max_length=3,
        choices=LANGUAGE_DIR_CHOICES,
        default=LTR,
    )

    def __str__(self):
        return self.language_code

    @property
    def general_language_code(self):
        return self.language_code[:2]

    def get_current_url(self, request):
        url = request.path
        return translate_url(url, self.language_code)

    class Meta:
        ordering = ('language_code',)
