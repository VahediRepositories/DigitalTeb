from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import inlineformset_factory
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, UpdateView, DetailView

from .forms import *
from .mixins import NonSpecialistForbiddenMixin
from ..accounts.views import RegistrationView, LoginRequiredMixin
from ..models import *
from ..modules import edition, pages
from ..multilingual.mixins import MultilingualViewMixin


class SpecialistSignUpView(RegistrationView):
    form_class = SpecialistCreationForm

    @property
    def template_name(self):
        return f'registration/{self.language_direction}/specialist_signup.html'

    def set_user_properties(self, user, form):
        specialty = form.cleaned_data['specialty']
        specialties.make_user_specialist(user, specialty)
        edition.make_user_editor(user)
        pages.create_specialist_page(user)
        bio = Biography(user=user)
        bio.save()


class SpecialistLabelsView(
    PermissionRequiredMixin,
    MultilingualViewMixin, TemplateView
):
    permission_required = ('home.add_label', 'home.change_label', 'home.delete_label')
    Formset = inlineformset_factory(
        User, Label, fields=('name', 'description'), extra=1, labels={
            'name': translation.gettext_lazy('name'),
            'description': translation.gettext_lazy('description')
        },
    )

    @property
    def template_name(self):
        return f'home/specialists/{self.language_direction}/labels_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = self.Formset(
            instance=self.request.user
        )
        return context

    def post(self, request, *args, **kwargs):
        formset = self.Formset(request.POST, instance=request.user)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(
                reverse('edit_labels')
            )
        else:
            context = {
                'formset': formset,
            }
            return self.render_to_response(context)


class TechnicalInformationView(
    LoginRequiredMixin,
    NonSpecialistForbiddenMixin,
    MultilingualViewMixin, TemplateView
):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['labels'] = Label.objects.filter(user=self.request.user)
        return context

    @property
    def template_name(self):
        return f'home/specialists/{self.language_direction}/career_edit.html'

    def get(self, *args, **kwargs):
        self.forbid_non_specialist()
        return super().get(*args, **kwargs)


class BiographyView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    NonSpecialistForbiddenMixin,
    MultilingualViewMixin, UpdateView
):
    model = Biography
    fields = ('biography',)
    success_url = reverse_lazy('edit_technical_info')
    success_message = translation.gettext_lazy(
        'Your biography was updated.'
    )

    @property
    def template_name(self):
        return f'home/specialists/{self.language_direction}/bio.html'

    def get(self, *args, **kwargs):
        self.forbid_non_specialist()
        return super().get(*args, **kwargs)


class PersonalPageView(
    MultilingualViewMixin, DetailView
):
    model = User

    @property
    def template_name(self):
        return f'home/specialists/{self.language_direction}/personal_page.html'
