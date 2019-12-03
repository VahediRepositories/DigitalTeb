from django import forms
from django.core.validators import RegexValidator
from django.utils import translation

from ...modules import sms


class PhoneField(forms.CharField):
    phone_validator = RegexValidator(
        regex=r'^((\+98)|(0))?\d{10}$'
    )

    def __init__(self, *args, **kwargs):
        super(PhoneField, self).__init__(*args, **kwargs)
        self.validators.append(self.phone_validator)
        self.label = translation.gettext_lazy('Cellphone Number')
        self.max_length = 20

    def clean(self, value):
        phone = super(PhoneField, self).clean(value)
        return phone[-10:]


class ConfirmationCodeField(forms.CharField):

    def __init__(self, *args, **kwargs):
        super(ConfirmationCodeField, self).__init__(*args, **kwargs)
        self.max_length = sms.CODE_LENGTH
        self.label = translation.gettext_lazy('Confirmation Code')
        self.help_text = translation.gettext_lazy(
            'Enter the %(num)d-digit code that was sent to you.'
        )
