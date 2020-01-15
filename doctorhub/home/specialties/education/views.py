from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils import translation
from django.views.generic import CreateView, UpdateView
from rest_framework import viewsets

from .serializers import *
from ...accounts.mixins import LoginRequiredMixin
from ...accounts.phone.mixins import CheckPhoneVerifiedMixin
from ...modules import authentication
from ...multilingual.mixins import MultilingualViewMixin
from ...permissions import *
from ...specialties.mixins import NonSpecialistForbiddenMixin
from ...specialties.permissions import *


class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = [
        IsSpecialistOrReadOnly & IsOwnerOrReadOnly,
    ]

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user,
        )


class EducationCreateView(
    LoginRequiredMixin,
    MultilingualViewMixin, NonSpecialistForbiddenMixin,
    CheckPhoneVerifiedMixin, CreateView
):
    model = Education
    fields = ['level', 'field', 'institution']

    def get_context_data(self, **kwargs):
        self.forbid_non_specialist()
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.forbid_non_specialist()
        education = form.save(commit=False)
        education.owner = self.request.user
        education.save()
        messages.success(
            self.request,
            translation.gettext('Education record was saved.'),
        )
        return HttpResponseRedirect(
            authentication.get_profile_url(self.request.user)
        )

    @property
    def template_name(self):
        return f'home/specialists/{self.language_direction}/education_create.html'


class EducationUpdateView(
    LoginRequiredMixin,
    MultilingualViewMixin, NonSpecialistForbiddenMixin,
    CheckPhoneVerifiedMixin, UpdateView
):
    model = Education
    fields = [
        'level', 'field', 'institution'
    ]

    def get_context_data(self, **kwargs):
        self.forbid_non_specialist()
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.forbid_non_specialist()
        form.save()
        messages.success(
            self.request,
            translation.gettext(
                'Education record was updated.'
            ),
            'successful-updated-education'
        )
        return HttpResponseRedirect(
            authentication.get_profile_url(self.request.user)
        )

    @property
    def template_name(self):
        return f'home/specialists/{self.language_direction}/education_edit.html'
