from django.utils import translation


class TranslatedField:
    def __init__(self, language_related_fields):
        self.language_related_fields = language_related_fields

    def __get__(self, instance, owner):
        if translation.get_language() == 'fr':
            return getattr(instance, self.fr_field)
        else:
            return getattr(instance, self.en_field)

