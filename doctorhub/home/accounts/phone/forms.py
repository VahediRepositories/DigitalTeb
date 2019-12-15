from django import forms

from .fields import PhoneField, ConfirmationCodeField
from .models import *


class ConfirmationCodeForm(forms.Form):
    confirmation_code = ConfirmationCodeField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['confirmation_code'].help_text = self.fields['confirmation_code'].help_text % {
            'num': CODE_LENGTH
        }


class PhoneUpdateForm(forms.ModelForm):
    number = PhoneField()

    class Meta:
        model = Phone
        fields = ['number']
