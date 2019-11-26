import datetime

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import GENDER_CHOICES
from .phone.fields import PhoneField
from ..modules import phones
from .phone.models import CODE_LENGTH


class UserCreationForm(auth_forms.UserCreationForm):
    first_name = forms.CharField(max_length=50, label='نام')
    last_name = forms.CharField(max_length=50, label='نام خانوادگى')
    gender = forms.ChoiceField(
        label='جنسيت', choices=GENDER_CHOICES
    )
    phone = PhoneField(
        label='شماره موبايل',
        max_length=20,
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

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phones.phone_exists(phone):
            raise ValidationError(
                'اين شماره قبلا ثبت شده است',
                code='invalid'
            )
        else:
            return phone

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name',
            'phone', 'gender', 'birthdate',
            'username', 'password1', 'password2',
            'captcha'
        ]


class ForgotAccountForm(forms.Form):
    phone = PhoneField(
        label='شماره موبايل',
        max_length=20,
        help_text='شماره موبايل خود را وارد كنيد'
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

    def clean_phone(self):
        phone_number = self.cleaned_data['phone']
        if not phones.verified_phone_exists(phone_number):
            raise ValidationError(
                'متاسفانه، اين شماره در ديجيتال طب ثبت نشده است.',
                code='invalid'
            )
        else:
            return phone_number


class PasswordChangeCodeForm(forms.Form):
    password_change_code = forms.CharField(
        max_length=CODE_LENGTH,
        label='كد تغيير رمز عبور',
        help_text=f'كد {CODE_LENGTH} رقمى اى كه برايتان ارسال شده است را وارد كنيد',
    )
