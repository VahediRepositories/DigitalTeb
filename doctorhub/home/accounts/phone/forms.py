from django import forms
from .models import *
from .fields import PhoneField


class ConfirmationCodeForm(forms.Form):
    confirmation_code = forms.CharField(
        max_length=CODE_LENGTH,
        label='كد فعال سازى',
        help_text=f'كد {CODE_LENGTH} رقمى اى كه برايتان ارسال شده است را وارد كنيد',
    )


class PhoneUpdateForm(forms.ModelForm):
    number = PhoneField(
        label='شماره موبايل',
        max_length=20,
    )

    class Meta:
        model = Phone
        fields = ['number']
