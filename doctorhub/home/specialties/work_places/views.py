from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, UpdateView, DetailView
from django.views.generic.base import View
from drf_multiple_model.pagination import MultipleModelLimitOffsetPagination
from drf_multiple_model.views import FlatMultipleModelAPIView
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from .mixins import *
from .permissions import *
from .serializers import *
from ..mixins import NonSpecialistForbiddenMixin
from ...accounts.views import LoginRequiredMixin
from ...models import *
from ...modules import pages
from ...permissions import *


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


class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    permission_classes = [
        IsPlaceOwnerOrReadOnly
    ]

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        place = serializer.validated_data['place']
        if place.has_staff(self.request.user):
            raise ValidationError(
                translation.gettext('Membership already exists')
            )
        elif Membership.objects.filter(
                employee=self.request.user, place=place, status=Membership.WAITING
        ).exists():
            raise ValidationError(
                translation.gettext('Membership request already sent')
            )
        else:
            serializer.save(
                employee=self.request.user
            )

    def perform_update(self, serializer):
        place = serializer.validated_data['place']
        if place.has_staff(self.request.user):
            raise ValidationError(
                translation.gettext('Membership already exists')
            )
        else:
            serializer.save(
                employee=self.request.user
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

    def get(self, request, *args, **kwargs):
        self.check_phone_verified(self.request)
        self.forbid_non_specialist()
        messages.warning(
            request=self.request,
            message=translation.gettext(
                'Your work place might have been already created by one of your colleagues.'
                ' If so, we highly recommend you to send a membership request,'
                ' instead of creating a duplicate place.'
                ' Please search medical centers'
                ' using our "Advanced Search Engine",'
                ' and make sure your work place does not exist before creating a new one.'
            ),
            extra_tags='work-place-might-added-before-warning'
        )
        return super().get(request, *args, **kwargs)

    @property
    def template_name(self):
        return f'home/specialists/{self.language_direction}/work_place_create.html'


class WorkPlaceView(
    LoginRequiredMixin,
    NonStaffForbiddenMixin,
    MultilingualViewMixin, CheckPhoneVerifiedMixin, DetailView
):
    model = WorkPlace

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        place = self.get_object()
        context['days'] = work_places.get_user_working_days(place, self.request.user)
        if self.request.user == place.owner:
            context['waiting_memberships'] = Membership.objects.filter(
                place=place, status=Membership.WAITING
            )
        return context

    @property
    def template_name(self):
        return f'home/specialists/{self.language_direction}/work_place.html'

    def get(self, request, *args, **kwargs):
        self.check_phone_verified(request)
        place = self.get_object()
        self.forbid_non_staff(place)
        notification_types_query = Q(
            verb=Membership.MEMBERSHIP_REQUEST
        ) | Q(
            verb=Membership.MEMBERSHIP_ACCEPTED
        ) | Q(
            verb=Membership.MEMBERSHIP_CANCELED
        )
        place.notifications.all().filter(
            recipient=request.user
        ).filter(notification_types_query).mark_all_as_read()
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
            {
                'queryset': MedicalCenter.objects.search(name=query),
                'serializer_class': MedicalCenterSerializer
            }
        ]
        return querylist


class AcceptMembershipView(
    LoginRequiredMixin,
    NonPlaceOwnerForbiddenMixin, View
):
    def post(self, request, *args, **kwargs):
        membership = get_object_or_404(
            Membership, pk=self.request.POST.get('membership', '')
        )
        self.forbid_non_owner(membership.place)
        membership.accept()
        return HttpResponse(status=204)


class RejectMembershipView(
    LoginRequiredMixin,
    NonPlaceOwnerForbiddenMixin, View
):
    def post(self, request, *args, **kwargs):
        membership = get_object_or_404(
            Membership, pk=self.request.POST.get('membership', '')
        )
        self.forbid_non_owner(membership.place)
        membership.reject()
        return HttpResponse(status=204)


class CancelMembershipView(
    LoginRequiredMixin,
    NonStaffForbiddenMixin, View
):
    def post(self, request, *args, **kwargs):
        membership = get_object_or_404(
            Membership, pk=self.request.POST.get('membership', '')
        )
        self.forbid_non_staff(membership.place)
        membership.cancel()
        return HttpResponse(status=204)
