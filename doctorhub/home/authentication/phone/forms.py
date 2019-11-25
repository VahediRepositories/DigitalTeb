from django import forms
from ..phone.models import CODE_LENGTH


class ConfirmationCodeForm(forms.Form):
    confirmation_code = forms.CharField(
        max_length=CODE_LENGTH,
        label='كد فعال سازى',
        help_text=f'كد {CODE_LENGTH} رقمى اى كه برايتان ارسال شده است را وارد كنيد',
    )
