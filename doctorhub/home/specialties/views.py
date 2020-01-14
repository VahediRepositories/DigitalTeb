from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView

from .forms import *
from .mixins import NonSpecialistForbiddenMixin
from ..accounts.views import RegistrationView, LoginRequiredMixin, ProfileUpdateView
from ..models import *
from ..modules import pages
from ..multilingual.mixins import MultilingualViewMixin


class SpecialistSignUpView(RegistrationView):
    form_class = SpecialistCreationForm

    @property
    def template_name(self):
        return f'registration/{self.language_direction}/specialist_signup.html'

    def set_user_properties(self, user, form):
        specialty = form.cleaned_data['specialty']
        specialties.make_user_specialist(user, specialty)
        pages.create_specialist_page(user)


class SpecialistProfileView(
    LoginRequiredMixin,
    NonSpecialistForbiddenMixin,
    MultilingualViewMixin, CheckPhoneVerifiedMixin, TemplateView
):

    @property
    def template_name(self):
        return f'home/specialists/{self.language_direction}/profile.html'

    def get(self, request, *args, **kwargs):
        self.forbid_non_specialist()
        self.check_phone_verified(request)
        return super().get(request, *args, **kwargs)


class SpecialistProfileUpdateView(
    NonSpecialistForbiddenMixin,
    ProfileUpdateView
):
    @property
    def template_name(self):
        return f'home/users/{self.language_direction}/specialist_profile_edit.html'

    def get(self, request, *args, **kwargs):
        self.forbid_non_specialist()
        return super().get(request, *args, **kwargs)

    def save_data(self):
        self.forbid_non_specialist()
        super().save_data()
        # updates personal page's title
        if 'username' in self.user_form.changed_data:
            for page in SpecialistPage.objects.filter(user=self.request.user):
                page.save()
