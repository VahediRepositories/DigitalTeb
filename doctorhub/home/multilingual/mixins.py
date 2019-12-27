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
        default_language = languages.get_default_language()
        if current_language != default_language:
            for field_name in field_names:
                default_field_name = f'{field_name}_{languages.get_translated_field_postfix(default_language)}'
                default_field = getattr(self, default_field_name)
                if not default_field:
                    current_field = getattr(
                        self,
                        f'{field_name}_{languages.get_translated_field_postfix(current_language)}'
                    )
                    setattr(self, default_field_name, current_field)
