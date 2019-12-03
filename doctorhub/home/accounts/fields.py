from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.utils import translation
from django.utils.functional import lazy
from ..modules import sms

reCaptchaField = ReCaptchaField(
    label=translation.gettext_lazy(
        'Prove that you are not a robot'
    ),
    widget=ReCaptchaV2Checkbox(
        attrs={
            'data-size': 'compact',
        },
        api_params={
            'hl': lazy(
                translation.get_language
            )()
        }
    )
)


class PasswordChangeCodeField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super(PasswordChangeCodeField, self).__init__(*args, **kwargs)
        self.max_length = sms.CODE_LENGTH
        self.label = translation.gettext_lazy('Password change code')
        self.help_text = translation.gettext_lazy(
            'Enter the %(num)d-digit code that was sent to you.'
        )
