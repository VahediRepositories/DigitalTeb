from django.db.models import Q
from django.utils import translation

from ..modules import languages


class MultilingualViewMixin:

    @property
    def language_direction(self):
        return self.language.direction

    @property
    def language(self):
        return languages.get_language()


class MultilingualModelMixin:

    def set_multilingual_fields(self, field_names):
        current_language = languages.get_language()
        for field_name in field_names:
            for language in languages.get_all_languages():
                translated_field_name = f'{field_name}_{languages.get_translated_field_postfix(language)}'
                translated_field = getattr(self, translated_field_name)
                if not translated_field:
                    current_field = getattr(
                        self, f'{field_name}_{languages.get_translated_field_postfix(current_language)}'
                    )
                    setattr(self, translated_field_name, current_field)

