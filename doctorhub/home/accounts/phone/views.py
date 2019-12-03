from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import translation
from django.views.generic import FormView
from django.views.generic.base import View

from .forms import ConfirmationCodeForm
from .mixins import ConfirmedForbiddenMixin
from ..mixins import LoginRequiredMixin
from ...models import DigitalTebPageMixin
from ...modules import sms
from ...multilingual.mixins import MultilingualViewMixin


class ConfirmationCodeView(
    SuccessMessageMixin, LoginRequiredMixin,
    ConfirmedForbiddenMixin, MultilingualViewMixin, FormView
):

    success_message = translation.gettext_lazy(
        'Your cell phone has verified successfully.'
    )
    form_class = ConfirmationCodeForm

    @property
    def template_name(self):
        return f'home/users/phone/{self.language_direction}/confirmation_code.html'

    def get_success_url(self):
        self.success_url = DigitalTebPageMixin.get_home_page().get_url()
        return super(ConfirmationCodeView, self).get_success_url()

    def get(self, request, *args, **kwargs):
        self.forbid_confirmed()
        return super(ConfirmationCodeView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        self.forbid_confirmed()
        code = form.cleaned_data['confirmation_code']
        verified = sms.verify_phone(self.request.user, code)
        if verified:
            return super(ConfirmationCodeView, self).form_valid(form)
        else:
            form.add_error(
                'confirmation_code', ValidationError(
                    translation.gettext(
                        'The entered code either is invalid or expired.'
                    )
                )
            )
            return super(ConfirmationCodeView, self).form_invalid(form)


class ResendConfirmationCodeView(LoginRequiredMixin, ConfirmedForbiddenMixin, View):

    def get(self, request, *args, **kwargs):
        self.forbid_confirmed()
        resent = sms.resend_confirmation_code(request.user)
        if resent:
            messages.success(
                request,
                translation.gettext('A confirmation code was sent to %(phone)s') % {
                    'phone': request.user.profile.phone.number
                }
            )
        else:
            messages.warning(
                request,
                translation.gettext(
                    'You need to wait %(num)d seconds to resend SMS.'
                ) % {
                    'num': sms.get_remained_confirmation_resend_time(request.user)
                },
            )
        return HttpResponseRedirect(reverse('confirmation_code'))
