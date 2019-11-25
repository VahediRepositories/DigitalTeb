import datetime

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.contrib.auth import forms as auth_forms
from django.core.exceptions import ValidationError

from ..users.phone.models import Phone
from .models import *


class UserCreationForm(auth_forms.UserCreationForm):
    first_name = forms.CharField(max_length=50, label='نام')
    last_name = forms.CharField(max_length=50, label='نام خانوادگى')
    gender = forms.ChoiceField(
        label='جنسيت', choices=GENDER_CHOICES
    )
    phone = forms.CharField(
        label='شماره موبايل',
        max_length=20,
        validators=[Phone.phone_validator]
    )
    birthdate = forms.DateField(
        label='تاريخ تولد', widget=forms.DateInput(
            attrs={
                'class': 'persian-datepicker'
            }
        )
    )

    captcha = ReCaptchaField(
        label='ثابت كنيد ربات نيستيد',
        widget=ReCaptchaV2Checkbox(
            attrs={
                'data-size': 'compact',
            },
            api_params={
                'hl': 'fa',
            }
        )
    )

    def clean_birthdate(self):
        birthdate = self.cleaned_data['birthdate']
        today = datetime.date.today()
        if birthdate >= today:
            raise ValidationError(
                forms.DateField.default_error_messages['invalid'], code='invalid'
            )
        else:
            return birthdate

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name',
            'phone', 'gender', 'birthdate',
            'username', 'password1', 'password2',
            'captcha'
        ]
