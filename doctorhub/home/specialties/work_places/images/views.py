from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from .serializers import *
from ..permissions import IsPlaceStaffOrReadOnly
from ....accounts.mixins import LoginRequiredMixin
from ..mixins import NonStaffForbiddenMixin
from ....accounts.phone.mixins import CheckPhoneVerifiedMixin


class PlaceImageViewSet(viewsets.ModelViewSet):
    queryset = WorkPlaceImage.objects.all()
    serializer_class = PlaceImageSerializer
    permission_classes = [
        IsPlaceStaffOrReadOnly,
    ]

    def perform_create(self, serializer):
        place = serializer.validated_data['place']
        if place.has_staff(self.request.user):
            return super().perform_create(serializer)
        else:
            raise ValidationError(translation.gettext('Non-staff users cannot add image'))

    def perform_update(self, serializer):
        place = serializer.validated_data['place']
        if place.has_staff(self.request.user):
            return super().perform_update(serializer)
        else:
            raise ValidationError(translation.gettext('Non-staff users cannot add image'))


class PlaceImageCreateView(
    LoginRequiredMixin, MultilingualViewMixin,
    NonStaffForbiddenMixin, CheckPhoneVerifiedMixin, CreateView
):
    model = WorkPlaceImage
    fields = [
        'image'
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
        place_image = form.save(commit=False)
        place_image.place = place
        place_image.save()
        messages.success(
            self.request, translation.gettext('Image Created!')
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
        return f'home/specialists/{self.language_direction}/place_image_create.html'


class PlaceImageUpdateView(
    LoginRequiredMixin, MultilingualViewMixin,
    NonStaffForbiddenMixin, CheckPhoneVerifiedMixin, UpdateView
):
    model = WorkPlaceImage
    fields = ['image']

    def get_context_data(self, **kwargs):
        self.check_phone_verified(self.request)
        self.forbid_non_staff(self.object.place)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.check_phone_verified(self.request)
        self.forbid_non_staff(self.object.place)
        form.save()
        messages.success(
            self.request, translation.gettext('Image Updated.')
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
        return f'home/specialists/{self.language_direction}/place_image_edit.html'
