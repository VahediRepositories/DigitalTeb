from django import forms

from ..modules import languages

LANGUAGE_CHOICES = [
    (
        lang.language_code,
        f'{lang.name} ({lang.language_code})'
    ) for lang in languages.get_all_languages()
]


class LanguageSettingsForm(forms.Form):
    language = forms.ChoiceField(
        choices=LANGUAGE_CHOICES,
        label='',
        widget=forms.Select(
            attrs={
                'class': 'lang-select'
            }
        )
    )
