from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils import translation
from django.views.generic import CreateView, UpdateView
from rest_framework import viewsets

from .serializers import *
from ...accounts.mixins import LoginRequiredMixin
from ...accounts.phone.mixins import CheckPhoneVerifiedMixin
from ...modules import authentication
from ...modules.specialties import services
from ...multilingual.mixins import MultilingualViewMixin
from ...permissions import *
from ...specialties.mixins import NonSpecialistForbiddenMixin
from ...specialties.permissions import *


class SymptomViewSet(viewsets.ModelViewSet):
    queryset = Symptom.objects.all()
    serializer_class = SymptomSerializer
    permission_classes = [
        IsSpecialistOrReadOnly & IsOwnerOrReadOnly,
    ]

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user,
        )


class SymptomCreateView(
    LoginRequiredMixin,
    MultilingualViewMixin, NonSpecialistForbiddenMixin,
    CheckPhoneVerifiedMixin, CreateView
):
    model = Symptom
    fields = ['name', 'description']

    def get_context_data(self, **kwargs):
        self.forbid_non_specialist()
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.forbid_non_specialist()
        service = form.save(commit=False)
        service.owner = self.request.user
        service.save()
        image_data = self.request.POST.get('image')
        if image_data:
            services.save_service_image(service, image_data)
        messages.success(
            self.request,
            translation.gettext('Symptom was saved.'),
        )
        return HttpResponseRedirect(
            authentication.get_profile_url(self.request.user)
        )

    @property
    def template_name(self):
        return f'home/specialists/{self.language_direction}/symptom_create.html'


class SymptomUpdateView(
    LoginRequiredMixin,
    MultilingualViewMixin, NonSpecialistForbiddenMixin,
    CheckPhoneVerifiedMixin, UpdateView
):
    model = Symptom
    fields = [
        'name', 'description'
    ]

    def get_context_data(self, **kwargs):
        self.forbid_non_specialist()
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.forbid_non_specialist()
        service = form.save()
        image_data = self.request.POST.get('image')
        if image_data:
            services.save_service_image(service, image_data)
        messages.success(
            self.request,
            translation.gettext(
                'Symptom was updated.'
            ),
            'successful-updated-service'
        )
        return HttpResponseRedirect(
            authentication.get_profile_url(self.request.user)
        )

    @property
    def template_name(self):
        return f'home/specialists/{self.language_direction}/symptom_edit.html'
