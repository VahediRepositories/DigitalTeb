from ..modules import languages


class MultilingualViewMixin:

    @property
    def language_direction(self):
        return self.language.direction

    @property
    def language(self):
        return languages.get_language()
