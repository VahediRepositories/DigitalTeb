from wagtail.core.models import Page
from ...modules import text_processing, languages


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
