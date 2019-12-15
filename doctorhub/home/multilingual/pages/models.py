from django.db import models
from wagtail.admin.edit_handlers import MultiFieldPanel
from wagtail.core.models import Page
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from ...modules import text_processing, languages
from ...multilingual.models import Language


class MultilingualPage(Page):

    def get_template_path(self, page_class):
        return f'home/{self.language_direction}/{self.get_template_name(page_class)}'

    @staticmethod
    def get_template_name(page_class):
        name = text_processing.upper_camel_to_snake(
            page_class.__name__
        )
        return f'{name}.html'

    @property
    def language(self):
        return languages.get_language()

    @property
    def language_direction(self):
        return self.language.direction

    class Meta:
        abstract = True


class MonolingualPage(MultilingualPage):
    language = models.ForeignKey(
        Language, on_delete=models.SET_NULL,
        null=True, blank=False
    )

    language_panel = MultiFieldPanel(
        [
            SnippetChooserPanel('language')
        ], heading='Languages', classname="collapsible collapsed"
    )

    def supports_language(self):
        return languages.get_language() == self.language

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['supported_languages'] = [self.language]
        return context

    class Meta:
        abstract = True
