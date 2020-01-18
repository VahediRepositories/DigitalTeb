from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DetailView
from drf_multiple_model.pagination import MultipleModelLimitOffsetPagination
from drf_multiple_model.views import FlatMultipleModelAPIView
from rest_framework import viewsets

from .mixins import NonStaffForbiddenMixin
from .permissions import *
from .serializers import *
from ..mixins import NonSpecialistForbiddenMixin
from ...accounts.phone.mixins import CheckPhoneVerifiedMixin
from ...accounts.views import LoginRequiredMixin
from ...modules.specialties import work_places
from ...multilingual.mixins import MultilingualViewMixin
from ...permissions import *
from ... import configurations


class WorkPlaceViewSet(viewsets.ModelViewSet):
    queryset = WorkPlace.objects.all()
    serializer_class = WorkPlaceSerializer
    permission_classes = [
        IsPlaceStaffOrReadOnly & (IsOwnerOrReadOnly | ~IsDelete),
    ]

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user,
        )


class WorkPlaceCreateView(
    LoginRequiredMixin,
    MultilingualViewMixin, NonSpecialistForbiddenMixin,
    CheckPhoneVerifiedMixin, CreateView
):
    model = WorkPlace
    fields = [
        'medical_center', 'name', 'city', 'region', 'address'
    ]

    def get_context_data(self, **kwargs):
        self.check_phone_verified(self.request)
        self.forbid_non_specialist()
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.check_phone_verified(self.request)
        self.forbid_non_specialist()
        place = form.save(commit=False)
        place.owner = self.request.user
        place.save()
        image_data = self.request.POST.get('image')
        if image_data:
            work_places.save_place_image(place, image_data)
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
    NonStaffForbiddenMixin,
    MultilingualViewMixin, CheckPhoneVerifiedMixin, DetailView
):
    model = WorkPlace

    @property
    def template_name(self):
        return f'home/specialists/{self.language_direction}/work_place.html'

    def get(self, request, *args, **kwargs):
        self.check_phone_verified(request)
        self.forbid_non_staff(self.get_object())
        return super().get(request, *args, **kwargs)


class WorkPlaceUpdateView(
    LoginRequiredMixin,
    MultilingualViewMixin, NonStaffForbiddenMixin,
    CheckPhoneVerifiedMixin, UpdateView
):
    model = WorkPlace
    fields = [
        'medical_center', 'name', 'city', 'region', 'address'
    ]

    def get_context_data(self, **kwargs):
        self.check_phone_verified(self.request)
        self.forbid_non_staff(self.object)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.forbid_non_specialist()
        place = form.save()
        image_data = self.request.POST.get('image')
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%', image_data)
        if image_data:
            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@', 'image sent')
            work_places.save_place_image(place, image_data)
        messages.success(
            self.request,
            translation.gettext(
                'Work Place was updated.'
            ),
            'successful-updated-work-place'
        )
        return HttpResponseRedirect(
            reverse('work_place_profile', kwargs={'pk': place.pk})
        )

    @property
    def template_name(self):
        return f'home/specialists/{self.language_direction}/work_place_edit.html'


class CitiesSearchPagination(MultipleModelLimitOffsetPagination):
    default_limit = configurations.SEARCH_LIMIT


class CitiesSearchView(FlatMultipleModelAPIView):
    pagination_class = CitiesSearchPagination

    def get_querylist(self):
        query = self.request.GET.get('search')
        querylist = [
            {
                'queryset': City.objects.search(name=query),
                'serializer_class': CitySerializer
            }
        ]
        return querylist


