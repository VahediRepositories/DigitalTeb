from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import translation
from django.views.generic import CreateView, UpdateView
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError


from .serializers import *
from ..permissions import *
from ....accounts.mixins import LoginRequiredMixin
from ....multilingual.mixins import MultilingualViewMixin
from ..mixins import NonStaffForbiddenMixin
from ....accounts.phone.mixins import CheckPhoneVerifiedMixin


class WorkPlacePhoneViewSet(viewsets.ModelViewSet):
    queryset = WorkPlacePhone.objects.all()
    serializer_class = WorkPlacePhoneSerializer
    permission_classes = [
        IsPlaceStaffOrReadOnly,
    ]

    def perform_create(self, serializer):
        place = serializer.validated_data['place']
        if place.has_staff(self.request.user):
            return super().perform_create(serializer)
        else:
            raise ValidationError(translation.gettext('Non-staff users cannot add phone'))

    def perform_update(self, serializer):
        place = serializer.validated_data['place']
        if place.has_staff(self.request.user):
            return super().perform_update(serializer)
        else:
            raise ValidationError(translation.gettext('Non-staff users cannot add phone'))


class PlacePhoneCreateView(
    LoginRequiredMixin, MultilingualViewMixin,
    NonStaffForbiddenMixin, CheckPhoneVerifiedMixin, CreateView
):
    model = WorkPlacePhone
    fields = [
        'phone_number'
    ]

    def get_place(self):
        return get_object_or_404(
            WorkPlace, pk=self.kwargs['place_pk']
        )

    def get_context_data(self, **kwargs):
        self.check_phone_verified(self.request)
        place = self.get_place()
        self.forbid_non_staff(place)
        context = super().get_context_data(**kwargs)
        context['place'] = place
        return context

    def form_valid(self, form):
        self.check_phone_verified(self.request)
        place = self.get_place()
        self.forbid_non_staff(place)
        phone = form.save(commit=False)
        phone.place = place
        phone.save()
        messages.success(
            self.request, translation.gettext('Phone Number Created.')
        )
        return HttpResponseRedirect(
            reverse(
                'work_place_profile', kwargs={
                    'pk': self.get_place().pk
                }
            )
        )

    @property
    def template_name(self):
        return f'home/specialists/{self.language_direction}/phone_create.html'


class PlacePhoneUpdateView(
    LoginRequiredMixin, MultilingualViewMixin,
    NonStaffForbiddenMixin, CheckPhoneVerifiedMixin, UpdateView
):

    model = WorkPlacePhone
    fields = ['phone_number']

    def get_place(self):
        return get_object_or_404(
            WorkPlace, pk=self.kwargs['place_pk']
        )

    def get_context_data(self, **kwargs):
        self.check_phone_verified(self.request)
        self.forbid_non_staff(self.object.place)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.check_phone_verified(self.request)
        self.forbid_non_staff(self.object.place)
        form.save()
        messages.success(
            self.request, translation.gettext('Phone Number Updated.')
        )
        return HttpResponseRedirect(
            reverse(
                'work_place_profile', kwargs={
                    'pk': self.object.place.pk
                }
            )
        )

    @property
    def template_name(self):
        return f'home/specialists/{self.language_direction}/phone_edit.html'
