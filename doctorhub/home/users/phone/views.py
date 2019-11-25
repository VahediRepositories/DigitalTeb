from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import FormView
from django.views.generic.base import View

from .forms import *
from .mixins import ConfirmedForbiddenMixin
from ...authentication.mixins import *
from ...models import DigitalTebPageMixin
from ...modules import sms


class ConfirmationCodeView(SuccessMessageMixin, LoginRequiredMixin, ConfirmedForbiddenMixin, FormView):
    form_class = ConfirmationCodeForm
    template_name = 'home/users/phone/confirmation_code.html'
    success_message = 'فعال سازى شماره موبايل شما با موفقيت انجام شد.'

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
                    'كد وارد شده يا اشتباه است و يا منقضى شده است.'
                )
            )
            return super(ConfirmationCodeView, self).form_invalid(form)


class ResendConfirmationCodeView(LoginRequiredMixin, ConfirmedForbiddenMixin, View):

    def get(self, request, *args, **kwargs):
        self.forbid_confirmed()
        resent = sms.resend_code(request.user)
        if resent:
            messages.success(
                request,
                'كد فعال سازى، به شماره ى {} ارسال شد.'.format(
                    request.user.profile.phone.number
                )
            )
        else:
            messages.warning(
                request,
                'براى ارسال مجدد پيامك بايد {} ثانيه صبر كنيد.'.format(
                    sms.get_remained_resend_time(request.user)
                )
            )
        return HttpResponseRedirect(reverse('confirmation_code'))
