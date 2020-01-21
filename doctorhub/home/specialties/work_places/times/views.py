from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, DetailView
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError as RestValidationError

from .serializers import *
from ..permissions import *
from ....accounts.mixins import LoginRequiredMixin
from ..mixins import NonStaffForbiddenMixin
from ....accounts.phone.mixins import CheckPhoneVerifiedMixin
from ....permissions import *


class WeekDayViewSet(viewsets.ModelViewSet):
    queryset = WeekDay.objects.all()
    serializer_class = WeekDaySerializer
    permission_classes = [
        IsPlaceStaffOrReadOnly & IsOwnerOrReadOnly,
    ]

    def perform_create(self, serializer):
        place = serializer.validated_data['place']
        if place.has_staff(self.request.user):
            return super().perform_create(serializer)
        else:
            raise RestValidationError(translation.gettext('Non-staff users cannot add week days'))

    def perform_update(self, serializer):
        place = serializer.validated_data['place']
        if place.has_staff(self.request.user):
            return super().perform_update(serializer)
        else:
            raise RestValidationError(translation.gettext('Non-staff users cannot add week days'))


class WeekDayCreateView(
    LoginRequiredMixin, MultilingualViewMixin,
    NonStaffForbiddenMixin, CheckPhoneVerifiedMixin, CreateView
):
    model = WeekDay
    fields = [
        'day'
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
        place = self.get_place()
        self.forbid_non_staff(place)
        week_day = form.save(commit=False)
        week_day.place = place
        week_day.owner = self.request.user
        if not WeekDay.objects.filter(
            place=week_day.place, owner=week_day.owner, day=week_day.day
        ).exists():
            week_day.save()
            messages.success(
                self.request, translation.gettext('Day Created!')
            )
            return HttpResponseRedirect(
                reverse(
                    'week-day', kwargs={
                        'pk': week_day.pk
                    }
                )
            )
        else:
            messages.error(
                self.request, translation.gettext('You cannot add duplicate days!')
            )
            return self.form_invalid(form)

    @property
    def template_name(self):
        return f'home/specialists/{self.language_direction}/week_day_create.html'


class WeekDayView(
    LoginRequiredMixin,
    NonStaffForbiddenMixin,
    MultilingualViewMixin, CheckPhoneVerifiedMixin, DetailView
):
    model = WeekDay

    @property
    def template_name(self):
        return f'home/specialists/{self.language_direction}/week_day.html'

    def get(self, request, *args, **kwargs):
        self.check_phone_verified(request)
        self.forbid_non_staff(self.get_object().place)
        return super().get(request, *args, **kwargs)
