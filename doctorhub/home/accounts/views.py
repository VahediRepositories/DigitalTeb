from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView
from django.views.generic.base import View, TemplateView

from .forms import *
from .mixins import AuthenticatedForbiddenMixin, LoginRequiredMixin
from .phone.forms import PhoneUpdateForm
from .phone.models import Phone
from ..models import DigitalTebPageMixin
from ..modules import authentication, sms, images
from ..multilingual.mixins import MultilingualViewMixin


class LoginView(
    SuccessMessageMixin, AuthenticatedForbiddenMixin,
    MultilingualViewMixin, auth_views.LoginView
):
    success_message = translation.gettext_lazy('Welcome!')

    @property
    def template_name(self):
        return f'registration/{self.language_direction}/login.html'

    def get(self, request, *args, **kwargs):
        self.forbid_authenticated()
        return super(LoginView, self).get(request, *args, **kwargs)


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):

    def get(self, request, *args, **kwargs):
        super(LogoutView, self).get(request, *args, **kwargs)
        messages.success(
            request,
            translation.gettext('You logged out of your account, successfully.'),
            extra_tags='successful-logout'
        )
        return HttpResponseRedirect(
            DigitalTebPageMixin.get_home_page().get_url()
        )


class SignUpView(AuthenticatedForbiddenMixin, MultilingualViewMixin, FormView):
    form_class = UserCreationForm
    success_url = reverse_lazy('profile')

    @property
    def template_name(self):
        return f'registration/{self.language_direction}/signup.html'

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
        success_message = translation.gettext(
            'Your account was created successfully. Now you can login.'
        )
        messages.success(
            request=self.request,
            message=success_message,
            extra_tags='successful-registration'
        )
        sms.send_confirmation_code(profile.phone)
        return super(SignUpView, self).form_valid(form)

    def set_user_groups(self, user):
        pass


class ForgotAccountView(AuthenticatedForbiddenMixin, MultilingualViewMixin, FormView):
    form_class = ForgotAccountForm

    @property
    def template_name(self):
        return f'registration/{self.language_direction}/forgot_account.html'

    def get(self, request, *args, **kwargs):
        self.forbid_authenticated()
        return super(ForgotAccountView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        self.forbid_authenticated()
        phone_number = form.cleaned_data['phone']
        success_message = translation.gettext(
            'A password change code was sent to %(phone)s'
        ) % {
                'phone': phone_number
        }
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


class PasswordChangeCodeView(AuthenticatedForbiddenMixin, MultilingualViewMixin, FormView):
    form_class = PasswordChangeCodeForm

    @property
    def template_name(self):
        return f'registration/{self.language_direction}/password_change_code.html'

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
                    translation.gettext(
                        'The entered code either is invalid or expired.'
                    )
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
                translation.gettext(
                    'A password change code was sent to %(phone)s'
                ) % {
                    'phone': phone
                }
            )
        else:
            messages.warning(
                request,
                translation.gettext(
                    'You need to wait %(num)d seconds to resend SMS.'
                ) % {
                    'num': sms.get_remained_password_change_resend_time(phone)
                },
            )
        return HttpResponseRedirect(
            reverse('password_change_code', args=[phone])
        )


class ResetPasswordView(AuthenticatedForbiddenMixin, MultilingualViewMixin, FormView):
    form_class = auth_forms.SetPasswordForm

    @property
    def template_name(self):
        return f'registration/{self.language_direction}/reset_password.html'

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
            translation.gettext(
                'Your password was changed successfully. Now you can login to you account.'
            ),
            'successful-password-reset'
        )
        return HttpResponseRedirect(
            DigitalTebPageMixin.get_home_page().get_url()
        )


class InvalidPasswordChangeCode(AuthenticatedForbiddenMixin, MultilingualViewMixin, TemplateView):

    @property
    def template_name(self):
        return f'registration/{self.language_direction}/invalid_password_change_code.html'

    def get(self, request, *args, **kwargs):
        self.forbid_authenticated()
        return super(InvalidPasswordChangeCode, self).get(request, *args, **kwargs)


class ProfileUpdateView(LoginRequiredMixin, MultilingualViewMixin, TemplateView):

    @property
    def template_name(self):
        return f'home/users/{self.language_direction}/profile_edit.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        context['user_form'] = UserUpdateForm(instance=self.request.user)
        context['profile_form'] = ProfileUpdateForm(instance=self.request.user.profile)
        context['phone_form'] = PhoneUpdateForm(instance=self.request.user.profile.phone)
        return context

    def post(self, request, *args, **kwargs):
        user_form = UserUpdateForm(
            request.POST, instance=request.user
        )
        profile_form = ProfileUpdateForm(
            request.POST, instance=request.user.profile
        )
        phone_form = PhoneUpdateForm(
            request.POST, instance=request.user.profile.phone
        )
        phone_number = request.user.profile.phone.number
        if user_form.is_valid() and profile_form.is_valid() and phone_form.is_valid():
            user_form.save()
            profile_form.save()
            phone = phone_form.save()
            if phone_number != phone.number:
                phone.verified = False
                phone.save()
                sms.send_confirmation_code(phone)
            image_data = self.request.POST.get('profile_image')
            if image_data:
                try:
                    file_name = f'{self.request.user.username}'

                    def save_profile_image(file_path, content_file):
                        self.request.user.profile.profile_image.save(
                            file_path, content_file, save=True
                        )

                    images.save_base64_to_file(file_name, image_data, save_profile_image)
                except Exception as e:
                    import traceback
                    traceback.print_exc()

            messages.success(
                request,
                translation.gettext(
                    'Your account information has updated.'
                ),
                'successful-profile-edit'
            )
            return HttpResponseRedirect(
                reverse('profile')
            )
        else:
            context = {
                'user_form': user_form,
                'profile_form': profile_form,
                'phone_form': phone_form,
            }
            return self.render_to_response(context)


class PasswordChangeView(
    LoginRequiredMixin, SuccessMessageMixin,
    MultilingualViewMixin, auth_views.PasswordChangeView
):

    @property
    def template_name(self):
        return f'home/users/{self.language_direction}/password_change.html'

    success_message = translation.gettext_lazy(
        'Your new password was submitted successfully.'
    )
    success_url = reverse_lazy('profile')


def email(request):
    subject = 'Thank you for registering to our site'
    message = ' it  means a world to us '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [request.GET['address'], ]
    res = send_mail(subject, message, email_from, recipient_list)
    return HttpResponse(res)

