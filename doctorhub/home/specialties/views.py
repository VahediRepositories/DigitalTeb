from django.contrib.messages.views import SuccessMessageMixin
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, FormView

from .forms import *
from .mixins import NonSpecialistForbiddenMixin
from ..accounts.views import RegistrationView, LoginRequiredMixin
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
        bio = Biography(user=user)
        bio.save()


class SpecialistInlineFormsetView(
    MultilingualViewMixin, NonSpecialistForbiddenMixin,
    CheckPhoneVerifiedMixin, TemplateView
):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = self.formset_class(
            instance=self.request.user
        )
        return context

    def get(self, request, *args, **kwargs):
        self.forbid_non_specialist()
        self.check_phone_verified(request)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.forbid_non_specialist()
        formset = self.formset_class(request.POST, instance=request.user)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(
                self.redirect_url
            )
        else:
            context = {
                'formset': formset,
            }
            return self.render_to_response(context)


class SpecialistLabelsView(SpecialistInlineFormsetView):
    formset_class = inlineformset_factory(
        User, Label, fields=('name', 'description'), extra=1, labels={
            'name': translation.gettext_lazy('name'),
            'description': translation.gettext_lazy('description')
        },
    )
    redirect_url = reverse_lazy('edit_labels')

    @property
    def template_name(self):
        return f'home/specialists/{self.language_direction}/labels_edit.html'


class SpecialistEducationView(SpecialistInlineFormsetView):
    formset_class = inlineformset_factory(
        User, Education, fields=('level', 'field', 'institution'), extra=1, labels={
            'level': translation.gettext_lazy('level'),
            'field': translation.gettext_lazy('field'),
            'institution': translation.gettext_lazy('institution'),
        },
    )
    redirect_url = reverse_lazy('edit_education')

    @property
    def template_name(self):
        return f'home/specialists/{self.language_direction}/education_edit.html'


class TechnicalInformationView(
    LoginRequiredMixin,
    NonSpecialistForbiddenMixin,
    MultilingualViewMixin, CheckPhoneVerifiedMixin, TemplateView
):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['labels'] = specialties.get_user_labels(
            self.request.user
        )
        return context

    @property
    def template_name(self):
        return f'home/specialists/{self.language_direction}/career_edit.html'

    def get(self, request, *args, **kwargs):
        self.forbid_non_specialist()
        self.check_phone_verified(request)
        return super().get(request, *args, **kwargs)


class BiographyView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    NonSpecialistForbiddenMixin,
    MultilingualViewMixin, CheckPhoneVerifiedMixin, UpdateView
):
    model = Biography
    fields = ('biography',)
    success_url = reverse_lazy('specialist_profile')
    success_message = translation.gettext_lazy(
        'Your biography was updated.'
    )

    @property
    def template_name(self):
        return f'home/specialists/{self.language_direction}/bio.html'

    def get(self, request, *args, **kwargs):
        self.forbid_non_specialist()
        self.check_phone_verified(request)
        return super().get(request, *args, **kwargs)


class SpecialistProfileView(
    LoginRequiredMixin,
    NonSpecialistForbiddenMixin,
    MultilingualViewMixin, CheckPhoneVerifiedMixin, TemplateView
):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    @property
    def template_name(self):
        return f'home/specialists/{self.language_direction}/profile.html'

    def get(self, request, *args, **kwargs):
        self.forbid_non_specialist()
        self.check_phone_verified(request)
        return super().get(request, *args, **kwargs)


class SpecialistArticlesView(
    LoginRequiredMixin,
    NonSpecialistForbiddenMixin,
    MultilingualViewMixin, CheckPhoneVerifiedMixin, FormView
):
    form_class = ArticleCreationForm

    @property
    def template_name(self):
        return f'home/specialists/{self.language_direction}/articles.html'

    def form_valid(self, form):
        self.forbid_non_specialist()
        category = form.cleaned_data['category']
        # TODO: use reverse to get the url
        return HttpResponseRedirect(
            f'/admin/pages/add/home/articlepage/{category.articlescategorypage.pk}/'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = ArticlePage.objects.filter(
            owner=self.request.user
        )
        return context

    def get(self, request, *args, **kwargs):
        self.forbid_non_specialist()
        self.check_phone_verified(request)
        return super().get(request, *args, **kwargs)
