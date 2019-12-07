from django.db import models
from wagtail.admin.edit_handlers import MultiFieldPanel
from wagtail.core.models import Page
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from ...modules import text_processing, languages
from ...multilingual.models import Language


class MultilingualPage(Page):

    @property
    def template(self):
        return f'home/{self.language_direction}/{self.template_name}'

    @property
    def template_name(self):
        name = text_processing.upper_camel_to_snake(
            self.__class__.__name__
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
        null=True, blank=True
    )

    language_panel = MultiFieldPanel(
        [
            SnippetChooserPanel('language')
        ], heading='Languages', classname="collapsible collapsed"
    )

    def supports_language(self):
        return languages.get_language() == self.language

    class Meta:
        abstract = True