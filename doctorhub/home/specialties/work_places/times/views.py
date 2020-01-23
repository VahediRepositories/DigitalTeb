from django.contrib import messages
from django.core.exceptions import PermissionDenied
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
from ....modules.specialties import work_places


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


class WorkTimeViewSet(viewsets.ModelViewSet):
    queryset = WorkTime.objects.all()
    serializer_class = WorkTimeSerializer
    permission_classes = [
        IsPlaceStaffOrReadOnly & IsOwnerOrReadOnly
    ]

    def perform_create(self, serializer):
        day = serializer.validated_data['day']
        place = day.place
        if place.has_staff(self.request.user) and day.owner == self.request.user:
            work_time = WorkTime(
                day=day, begin=serializer.validated_data['begin'], end=serializer.validated_data['end']
            )
            if work_places.is_working_time_valid(work_time):
                return super().perform_create(serializer)
            else:
                raise RestValidationError(
                    translation.gettext("Work time is invalid")
                )
        else:
            raise RestValidationError(
                translation.gettext("You don't have permission to add this work time")
            )

    def perform_update(self, serializer):
        day = serializer.validated_data['day']
        place = day.place
        if place.has_staff(self.request.user) and day.owner == self.request.user:
            work_time = WorkTime(
                day=day, begin=serializer.validated_data['begin'], end=serializer.validated_data['end']
            )
            if work_places.is_working_time_valid(work_time):
                return super().perform_update(serializer)
            else:
                raise RestValidationError(
                    translation.gettext('Work time is invalid')
                )
        else:
            return RestValidationError(
                translation.gettext("You don't have permission to update this work time")
            )


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


class WorkTimeCreateView(
    LoginRequiredMixin, MultilingualViewMixin,
    NonStaffForbiddenMixin, CheckPhoneVerifiedMixin, CreateView
):
    model = WorkTime
    fields = [
        'begin', 'end'
    ]

    def form_valid(self, form):
        day = self.get_day()
        place = day.place
        self.forbid_non_staff(place)
        if day.owner != self.request.user:
            raise PermissionDenied
        work_time = form.save(commit=False)
        work_time.day = day
        if work_places.is_working_time_valid(work_time):
            work_time.save()
            messages.success(
                self.request, translation.gettext('Time Interval Created!')
            )
            return HttpResponseRedirect(
                reverse(
                    'week-day', kwargs={
                        'pk': day.pk
                    }
                )
            )
        else:
            messages.error(
                self.request, translation.gettext('Invalid Time Interval!')
            )
            return self.form_invalid(form)

    def get_day(self):
        return get_object_or_404(
            WeekDay, pk=self.kwargs['day_pk']
        )

    def get_context_data(self, **kwargs):
        self.check_phone_verified(self.request)
        day = self.get_day()
        place = day.place
        self.forbid_non_staff(place)
        context = super().get_context_data(**kwargs)
        context['day'] = day
        context['intervals'] = WorkTime.objects.filter(day=day)
        return context

    @property
    def template_name(self):
        return f'home/specialists/{self.language_direction}/work_time_create.html'


class WeekDayView(
    LoginRequiredMixin,
    NonStaffForbiddenMixin,
    MultilingualViewMixin, CheckPhoneVerifiedMixin, DetailView
):
    model = WeekDay

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(
            reverse(
                'create_work_time', kwargs={
                    'day_pk': self.get_object().pk
                }
            )
        )

    @property
    def template_name(self):
        return f'home/specialists/{self.language_direction}/week_day.html'

    def get_context_data(self, **kwargs):
        self.check_phone_verified(self.request)
        self.forbid_non_staff(self.get_object().place)
        if self.object.owner != self.request.user:
            raise PermissionDenied
        context = super().get_context_data(**kwargs)
        context['intervals'] = WorkTime.objects.filter(day=self.object)
        return context
