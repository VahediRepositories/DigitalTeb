from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import FormView
from django.views.generic.base import View, TemplateView

from .forms import *
from .mixins import AuthenticatedForbiddenMixin, LoginRequiredMixin
from .phone.forms import PhoneUpdateForm
from .phone.models import Phone
from ..accounts.phone.mixins import CheckPhoneVerifiedMixin
from ..modules import authentication, sms, images, pages
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
        return super().get(request, *args, **kwargs)


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        messages.success(
            request,
            translation.gettext('You logged out of your account, successfully.'),
            extra_tags='successful-logout'
        )
        return HttpResponseRedirect(
            pages.get_home_page().get_url()
        )


class RegistrationView(AuthenticatedForbiddenMixin, MultilingualViewMixin, FormView):

    def get(self, request, *args, **kwargs):
        self.forbid_authenticated()
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return pages.get_home_page().get_url()

    def form_valid(self, form):
        self.forbid_authenticated()
        user = form.save()
        # user.first_name = form.cleaned_data['first_name']
        # user.last_name = form.cleaned_data['last_name']
        # user.save()
        profile = authentication.create_profile(user, form)

        self.set_user_properties(user, form)

        success_message = translation.gettext(
            'Your account was created successfully. Now you can login.'
        )
        messages.success(
            request=self.request,
            message=success_message,
            extra_tags='successful-registration'
        )
        sms.send_confirmation_code(profile.phone)
        return super().form_valid(form)

    def set_user_properties(self, user, form):
        pass


class SignUpView(RegistrationView):
    form_class = UserCreationForm

    @property
    def template_name(self):
        return f'registration/{self.language_direction}/signup.html'

    def set_user_properties(self, user, form):
        profile = user.profile
        profile.save()
        BirthDate(
            user=user, birthdate=form.cleaned_data['birthdate']
        ).save()


class ForgotAccountView(AuthenticatedForbiddenMixin, MultilingualViewMixin, FormView):
    form_class = ForgotAccountForm

    @property
    def template_name(self):
        return f'registration/{self.language_direction}/forgot_account.html'

    def get(self, request, *args, **kwargs):
        self.forbid_authenticated()
        return super().get(request, *args, **kwargs)

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
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
            return super().form_invalid(form)


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
            return super().get(request, *args, **kwargs)
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
        context = super().get_context_data(**kwargs)
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
            pages.get_home_page().get_url()
        )


class InvalidPasswordChangeCode(AuthenticatedForbiddenMixin, MultilingualViewMixin, TemplateView):

    @property
    def template_name(self):
        return f'registration/{self.language_direction}/invalid_password_change_code.html'

    def get(self, request, *args, **kwargs):
        self.forbid_authenticated()
        return super().get(request, *args, **kwargs)


class ProfileUpdateView(
    LoginRequiredMixin, MultilingualViewMixin,
    CheckPhoneVerifiedMixin, TemplateView
):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserUpdateForm(instance=self.request.user)
        context['profile_form'] = ProfileUpdateForm(instance=self.request.user.profile)
        context['phone_form'] = PhoneUpdateForm(instance=self.request.user.profile.phone)
        return context

    def get_context_data_after_post(self):
        return {
            'user_form': self.user_form,
            'profile_form': self.profile_form,
            'phone_form': self.phone_form,
        }

    def get(self, request, *args, **kwargs):
        self.check_phone_verified(request)
        return super().get(request, *args, **kwargs)

    @property
    def user_form(self):
        return UserUpdateForm(
            self.request.POST, instance=self.request.user
        )

    @property
    def profile_form(self):
        return ProfileUpdateForm(
            self.request.POST, instance=self.request.user.profile
        )

    @property
    def phone_form(self):
        return PhoneUpdateForm(
            self.request.POST, instance=self.request.user.profile.phone
        )

    def are_valid(self):
        return self.user_form.is_valid() and self.profile_form.is_valid() and self.phone_form.is_valid()

    def save_data(self):
        phone_number = self.request.user.profile.phone.number
        self.user_form.save()
        self.profile_form.save()
        phone = self.phone_form.save()
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

    def post(self, request, *args, **kwargs):
        if self.are_valid():
            self.save_data()
            messages.success(
                request,
                translation.gettext(
                    'Your account information has updated.'
                ),
                'successful-profile-edit'
            )
            return HttpResponseRedirect(
                authentication.get_profile_url(request.user)
            )
        else:
            context = self.get_context_data_after_post()
            return self.render_to_response(context)


class UserProfileUpdateView(ProfileUpdateView):
    @property
    def template_name(self):
        return f'home/users/{self.language_direction}/profile_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['birthdate_form'] = BirthdateUpdateForm(instance=self.request.user.birthdate)
        return context

    @property
    def birthdate_form(self):
        return BirthdateUpdateForm(
            self.request.POST, instance=self.request.user.birthdate
        )

    def get_context_data_after_post(self):
        context = super().get_context_data_after_post()
        context['birthdate_form'] = self.birthdate_form
        return context

    def are_valid(self):
        return super().are_valid() and self.birthdate_form.is_valid()

    def save_data(self):
        super().save_data()
        self.birthdate_form.save()


class PasswordChangeView(
    LoginRequiredMixin, SuccessMessageMixin,
    MultilingualViewMixin, CheckPhoneVerifiedMixin, auth_views.PasswordChangeView
):

    def get(self, request, *args, **kwargs):
        self.check_phone_verified(request)
        return super().get(request, *args, **kwargs)

    @property
    def template_name(self):
        return f'home/users/{self.language_direction}/password_change.html'

    def get_success_url(self):
        return authentication.get_profile_url(self.request.user)

    success_message = translation.gettext_lazy(
        'Your new password was submitted successfully.'
    )
