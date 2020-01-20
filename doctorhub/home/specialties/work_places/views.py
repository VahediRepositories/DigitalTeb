from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DetailView
from drf_multiple_model.pagination import MultipleModelLimitOffsetPagination
from drf_multiple_model.views import FlatMultipleModelAPIView
from rest_framework import viewsets

from .mixins import NonStaffForbiddenMixin
from .permissions import *
from .serializers import *
from ..mixins import NonSpecialistForbiddenMixin
from ...accounts.views import LoginRequiredMixin
from ...models import *
from ...permissions import *
from ...modules import pages


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
        new_page = WorkPlacePage(place=place)
        parent_page = pages.get_medical_centers_page()
        pages.create_page(parent_page, new_page)
        messages.success(
            self.request, translation.gettext('Work Place Created!')
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
        if image_data:
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


class SearchMedicalCentersPagination(MultipleModelLimitOffsetPagination):
    default_limit = configurations.SEARCH_LIMIT


class SearchMedicalCentersView(FlatMultipleModelAPIView):
    pagination_class = SearchMedicalCentersPagination

    def get_querylist(self):
        query = self.request.GET.get('search')
        city = self.request.GET.get('city')
        querylist = [
            {
                'queryset': WorkPlace.objects.search(name=query, city=city),
                'serializer_class': WorkPlaceSerializer
            },
            # {
            #     'queryset': Specialty.objects.search(name=query),
            #     'serializer_class': SpecialtySerializer
            # }
        ]
        return querylist


