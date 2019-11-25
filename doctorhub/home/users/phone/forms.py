from django import forms
from . import configurations


class ConfirmationCodeForm(forms.Form):
    confirmation_code = forms.CharField(
        max_length=configurations.CONFIRMATION_CODE_LENGTH,
        label='كد فعال سازى',
        help_text=f'كد {configurations.CONFIRMATION_CODE_LENGTH} رقمى اى كه برايتان ارسال شده است را وارد كنيد',
    )
