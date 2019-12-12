from django import forms

from .models import *
from ..accounts.forms import RegistrationForm


class SpecialistCreationForm(RegistrationForm):
    specialty = forms.ChoiceField(
        # Translators: This appears on registration page where specialists have to select their specialty.
        label=translation.gettext_lazy('Specialty'),
    )

    def __init__(self, *args, **kwargs):
        super(SpecialistCreationForm, self).__init__(*args, **kwargs)
        specialty_choices = [
            (specialty.default_name, specialty.name)
            for specialty in Specialty.objects.all()
        ]
        self.fields['specialty'].choices = specialty_choices

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name',
            'phone', 'gender', 'specialty',
            'username', 'password1', 'password2',
            'captcha'
        ]

