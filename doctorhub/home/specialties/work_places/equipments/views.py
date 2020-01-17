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
from ....modules.specialties import equipments


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [
        IsPlaceStaffOrReadOnly,
    ]

    def perform_create(self, serializer):
        place = serializer.validated_data['place']
        if place.has_staff(self.request.user):
            return super().perform_create(serializer)
        else:
            raise ValidationError(translation.gettext('Non-staff users cannot add equipment.'))

    def perform_update(self, serializer):
        place = serializer.validated_data['place']
        if place.has_staff(self.request.user):
            return super().perform_update(serializer)
        else:
            raise ValidationError(translation.gettext('Non-staff users cannot add equipment.'))


class EquipmentCreateView(
    LoginRequiredMixin,
    MultilingualViewMixin, NonStaffForbiddenMixin,
    CheckPhoneVerifiedMixin, CreateView
):
    model = Equipment
    fields = ['name', 'description']

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
        place = self.get_place()
        self.forbid_non_staff(place)
        equipment = form.save(commit=False)
        equipment.place = place
        equipment.save()
        image_data = self.request.POST.get('image')
        if image_data:
            equipments.save_equipment_image(equipment, image_data)
        messages.success(
            self.request,
            translation.gettext('Equipment Created!'),
        )
        return HttpResponseRedirect(
            reverse(
                'work_place_profile', kwargs={'pk': place.pk}
            )
        )

    @property
    def template_name(self):
        return f'home/specialists/{self.language_direction}/equipment_create.html'


class EquipmentUpdateView(
    LoginRequiredMixin,
    MultilingualViewMixin, NonStaffForbiddenMixin,
    CheckPhoneVerifiedMixin, UpdateView
):
    model = Equipment
    fields = [
        'name', 'description'
    ]

    def get_context_data(self, **kwargs):
        self.check_phone_verified(self.request)
        self.forbid_non_staff(self.object.place)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.forbid_non_staff(self.object.place)
        equipment = form.save()
        image_data = self.request.POST.get('image')
        if image_data:
            equipments.save_equipment_image(equipment, image_data)
        messages.success(
            self.request,
            translation.gettext(
                'Equipment updated!'
            ),
        )
        return HttpResponseRedirect(
            reverse(
                'work_place_profile', kwargs={
                    'pk': equipment.place.pk
                }
            )
        )

    @property
    def template_name(self):
        return f'home/specialists/{self.language_direction}/equipment_edit.html'
