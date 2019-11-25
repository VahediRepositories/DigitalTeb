from django import forms
from django.core.validators import RegexValidator


class PhoneField(forms.CharField):
    phone_validator = RegexValidator(
        regex=r'^((\+98)|(0))?\d{10}$'
    )

    def __init__(self, *args, **kwargs):
        super(PhoneField, self).__init__(*args, **kwargs)
        self.validators.append(self.phone_validator)

    def clean(self, value):
        phone = super(PhoneField, self).clean(value)
        return phone[-10:]