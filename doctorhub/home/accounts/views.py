from django.contrib import messages
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import FormView
from django.views.generic.base import View, TemplateView

from .forms import UserCreationForm, ForgotAccountForm, PasswordChangeCodeForm
from .mixins import AuthenticatedForbiddenMixin, LoginRequiredMixin
from .phone.models import Phone
from ..models import DigitalTebPageMixin
from ..modules import authentication, sms


class LoginView(SuccessMessageMixin, AuthenticatedForbiddenMixin, auth_views.LoginView):
    success_message = 'خوش آمديد!'

    def get(self, request, *args, **kwargs):
        self.forbid_authenticated()
        return super(LoginView, self).get(request, *args, **kwargs)


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):

    def get(self, request, *args, **kwargs):
        super(LogoutView, self).get(request, *args, **kwargs)
        messages.success(
            request,
            'با موفقيت از حساب كاربرى خود خارج شديد.',
            extra_tags='successful-logout'
        )
        return HttpResponseRedirect(
            DigitalTebPageMixin.get_home_page().get_url()
        )


class SignUpView(AuthenticatedForbiddenMixin, FormView):
    template_name = 'registration/signup.html'
    form_class = UserCreationForm

    def get_success_url(self):
        self.success_url = DigitalTebPageMixin.get_home_page().get_url()
        return super(SignUpView, self).get_success_url()

    def get(self, request, *args, **kwargs):
        self.forbid_authenticated()
        return super(SignUpView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        self.forbid_authenticated()
        user = form.save()
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()
        profile = authentication.create_profile(user, form)
        self.set_user_groups(user)
        success_message = 'حساب كاربرى شما با موفقيت ايجاد شد. اكنون ميتوانيد وارد شويد.'
        messages.success(
            request=self.request,
            message=success_message,
            extra_tags='successful-registration'
        )
        sms.send_confirmation_code(profile.phone)
        return super(SignUpView, self).form_valid(form)

    def set_user_groups(self, user):
        pass


class ForgotAccountView(AuthenticatedForbiddenMixin, FormView):
    template_name = 'registration/forgot_account.html'
    form_class = ForgotAccountForm

    def get(self, request, *args, **kwargs):
        self.forbid_authenticated()
        return super(ForgotAccountView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        self.forbid_authenticated()
        phone_number = form.cleaned_data['phone']
        success_message = 'پيامكى حاوى كد تغيير رمز عبور به شماره ى {} ارسال شد.'.format(
            phone_number
        )
        messages.success(
            request=self.request,
            message=success_message,
            extra_tags='successful-password-change-code-sent'
        )
        phone = Phone.objects.get(number=phone_number)
        sms.send_password_change_code(phone)
        return HttpResponseRedirect(
            reverse(
                'password_change_code', args=[phone_number]
            )
        )


class PasswordChangeCodeView(AuthenticatedForbiddenMixin, FormView):
    template_name = 'registration/password_change_code.html'
    form_class = PasswordChangeCodeForm

    def get(self, request, *args, **kwargs):
        self.forbid_authenticated()
        return super(PasswordChangeCodeView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PasswordChangeCodeView, self).get_context_data(**kwargs)
        context['phone'] = self.kwargs['phone']
        return context

    def form_valid(self, form):
        self.forbid_authenticated()
        code = form.cleaned_data['password_change_code']
        phone = self.kwargs['phone']
        verified = authentication.verify_password_change_code(phone, code)
        if verified:
            return HttpResponseRedirect(
                reverse(
                    'reset_password', args=[phone, code]
                )
            )
        else:
            form.add_error(
                'password_change_code', ValidationError(
                    'كد وارد شده يا اشتباه است و يا منقضى شده است.'
                )
            )
            return super(PasswordChangeCodeView, self).form_invalid(form)


class ResendPasswordChangeCodeView(AuthenticatedForbiddenMixin, View):

    def get(self, request, *args, **kwargs):
        self.forbid_authenticated()
        phone = self.kwargs['phone']
        resent = sms.resend_password_change_code(phone)
        if resent:
            messages.success(
                request,
                'كد تغيير رمز عبور، به شماره ى {} ارسال شد.'.format(phone)
            )
        else:
            messages.warning(
                request,
                'براى ارسال مجدد پيامك بايد {} ثانيه صبر كنيد.'.format(
                    sms.get_remained_password_change_resend_time(phone)
                )
            )
        return HttpResponseRedirect(
            reverse('password_change_code', args=[phone])
        )


class ResetPasswordView(AuthenticatedForbiddenMixin, FormView):
    form_class = auth_forms.SetPasswordForm
    template_name = 'registration/reset_password.html'

    def get(self, request, *args, **kwargs):
        self.forbid_authenticated()
        code = self.kwargs['code']
        phone = self.kwargs['phone']
        verified = authentication.verify_password_change_code(phone, code)
        if verified:
            return super(ResetPasswordView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(
                reverse(
                    'invalid_password_change_code', args=[phone, code]
                )
            )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.get_user()
        return kwargs

    def get_user(self):
        phone = self.kwargs['phone']
        return Phone.get_user_by_phone_number(phone)

    def get_context_data(self, **kwargs):
        context = super(ResetPasswordView, self).get_context_data(**kwargs)
        context['user'] = self.get_user()
        return context

    def form_valid(self, form):
        self.forbid_authenticated()
        form.save()
        authentication.use_password_change_code(
            self.get_user(), self.kwargs['code']
        )
        messages.success(
            self.request,
            'تغيير رمز عبور شما با موفقيت انجام شد. اكنون ميتوانيد وارد حساب كاربرى خود شويد.',
            'successful-password-reset'
        )
        return HttpResponseRedirect(
            DigitalTebPageMixin.get_home_page().get_url()
        )


class InvalidPasswordChangeCode(AuthenticatedForbiddenMixin, TemplateView):
    template_name = 'registration/invalid_password_change_code.html'

    def get(self, request, *args, **kwargs):
        self.forbid_authenticated()
        return super(InvalidPasswordChangeCode, self).get(request, *args, **kwargs)