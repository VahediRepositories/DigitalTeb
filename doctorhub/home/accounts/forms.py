import datetime

from django import forms
from django.contrib.auth import forms as auth_forms
from django.core.exceptions import ValidationError

from .fields import reCaptchaField, PasswordChangeCodeField
from .models import *
from .phone.fields import PhoneField
from .phone.models import CODE_LENGTH
from ..modules import phones


class RegistrationForm(auth_forms.UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    gender = forms.ChoiceField(
        # Translators: This appears on registration page where users have to select their sex.
        label=translation.gettext_lazy('Sex'),
        choices=GENDER_CHOICES
    )
    phone = PhoneField()
    captcha = reCaptchaField

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phones.phone_exists(phone):
            raise ValidationError(
                translation.gettext('The phone number is already taken.'),
                code='invalid'
            )
        else:
            return phone


class UserCreationForm(RegistrationForm):
    birthdate = forms.DateField(
        label=translation.gettext_lazy('Birthdate'),
        widget=forms.DateInput(
            attrs={
                'class': 'persian-datepicker'
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


class ForgotAccountForm(forms.Form):
    phone = PhoneField(
        help_text=translation.gettext_lazy('Enter you cell phone number.')
    )

    captcha = reCaptchaField

    def clean_phone(self):
        phone_number = self.cleaned_data['phone']
        if not phones.verified_phone_exists(phone_number):
            raise ValidationError(
                translation.gettext('Unfortunately, the phone number is not registered.'),
                code='invalid'
            )
        else:
            return phone_number


class PasswordChangeCodeForm(forms.Form):
    password_change_code = PasswordChangeCodeField()

    def __init__(self, *args, **kwargs):
        super(PasswordChangeCodeForm, self).__init__(*args, **kwargs)
        self.fields['password_change_code'].help_text = self.fields['password_change_code'].help_text % {
            'num': CODE_LENGTH
        }


class UserUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'gender',
            'birthdate'
        ]
        labels = {
            'gender': translation.gettext_lazy('Sex'),
            'birthdate': translation.gettext_lazy('Birthdate')
        }
        widgets = {
            'birthdate': forms.DateInput(
                attrs={
                    'class': 'persian-datepicker'
                }
            )
        }
