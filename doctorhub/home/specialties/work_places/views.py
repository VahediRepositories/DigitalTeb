from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, TemplateView, DetailView
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from .serializers import *
from ...accounts.phone.mixins import CheckPhoneVerifiedMixin
from ...accounts.views import LoginRequiredMixin
from ...modules.specialties import work_places
from ...multilingual.mixins import MultilingualViewMixin
from ...specialties.mixins import NonSpecialistForbiddenMixin
from ...specialties.permissions import *
from ...permissions import *
from .permissions import *
from ...modules import authentication


class WorkPlaceViewSet(viewsets.ModelViewSet):
    queryset = WorkPlace.objects.all()
    serializer_class = WorkPlaceSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsSpecialistOrReadOnly,
        IsOwnerOrReadOnly,
    ]

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user,
        )


class WorkPlacePhoneViewSet(viewsets.ModelViewSet):
    queryset = WorkPlacePhone.objects.all()
    serializer_class = WorkPlacePhoneSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsSpecialistOrReadOnly,
        IsWorkPlaceStaffOrReadOnly,
    ]

    def perform_create(self, serializer):
        place = serializer.validated_data['place']
        if place.owner == self.request.user:
            return super().perform_create(serializer)
        else:
            raise ValidationError(translation.gettext('Non-staff users cannot add phone'))


class WorkPlaceCreateView(
    LoginRequiredMixin,
    MultilingualViewMixin, NonSpecialistForbiddenMixin,
    CheckPhoneVerifiedMixin, CreateView
):
    model = WorkPlace
    fields = [
        'medical_center', 'name', 'address', 'city'
    ]

    def get_context_data(self, **kwargs):
        self.forbid_non_specialist()
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.forbid_non_specialist()
        place = form.save(commit=False)
        place.owner = self.request.user
        place.save()
        image_data = self.request.POST.get('logo_image')
        if image_data:
            work_places.save_place_logo_image(place, image_data)
        messages.success(
            self.request, translation.gettext('Work Place was saved')
        )
        return HttpResponseRedirect(
            reverse('work_place_profile', kwargs={'pk': place.pk})
        )

    @property
    def template_name(self):
        return f'home/specialists/{self.language_direction}/work_place_create.html'


class WorkPlaceView(
    LoginRequiredMixin,
    NonSpecialistForbiddenMixin,
    MultilingualViewMixin, CheckPhoneVerifiedMixin, DetailView
):

    model = WorkPlace

    @property
    def template_name(self):
        return f'home/specialists/{self.language_direction}/work_place.html'

    def get(self, request, *args, **kwargs):
        self.forbid_non_specialist()
        self.check_phone_verified(request)
        return super().get(request, *args, **kwargs)


class SpecialistWorkPlaceUpdateView(
    LoginRequiredMixin,
    MultilingualViewMixin, NonSpecialistForbiddenMixin,
    CheckPhoneVerifiedMixin, UpdateView
):
    model = WorkPlace
    fields = [
        'medical_center', 'name', 'address', 'city'
    ]

    def get_context_data(self, **kwargs):
        self.forbid_non_specialist()
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.forbid_non_specialist()
        place = form.save()
        image_data = self.request.POST.get('logo_image')
        if image_data:
            work_places.save_place_logo_image(place, image_data)
        messages.success(
            self.request,
            translation.gettext(
                'Work Place was updated.'
            ),
            'successful-updated-work-place'
        )
        return HttpResponseRedirect(
            authentication.get_profile_url(self.request.user)
        )

    @property
    def template_name(self):
        return f'home/specialists/{self.language_direction}/work_place_edit.html'
