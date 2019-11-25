from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.views.generic import FormView

from .forms import UserCreationForm
from .mixins import *
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
        sms.send_confirmation_sms(profile.phone)
        return super(SignUpView, self).form_valid(form)

    def set_user_groups(self, user):
        pass
