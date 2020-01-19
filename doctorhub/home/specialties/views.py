from django.views.generic import TemplateView
from drf_multiple_model.pagination import MultipleModelLimitOffsetPagination
from drf_multiple_model.views import FlatMultipleModelAPIView

from .forms import *
from .mixins import NonSpecialistForbiddenMixin
from .serializers import *
from ..accounts.serializers import *
from ..accounts.views import RegistrationView, LoginRequiredMixin, ProfileUpdateView
from ..models import *


class SpecialistSignUpView(RegistrationView):
    form_class = SpecialistCreationForm

    @property
    def template_name(self):
        return f'registration/{self.language_direction}/specialist_signup.html'

    def set_user_properties(self, user, form):
        specialty = form.cleaned_data['specialty']
        specialties.make_user_specialist(user, specialty)
        pages.create_specialist_page(user)


class SpecialistProfileView(
    LoginRequiredMixin,
    NonSpecialistForbiddenMixin,
    MultilingualViewMixin, CheckPhoneVerifiedMixin, TemplateView
):

    @property
    def template_name(self):
        return f'home/specialists/{self.language_direction}/profile.html'

    def get(self, request, *args, **kwargs):
        self.forbid_non_specialist()
        self.check_phone_verified(request)
        return super().get(request, *args, **kwargs)


class SpecialistProfileUpdateView(
    NonSpecialistForbiddenMixin,
    ProfileUpdateView
):
    @property
    def template_name(self):
        return f'home/users/{self.language_direction}/specialist_profile_edit.html'

    def get(self, request, *args, **kwargs):
        self.forbid_non_specialist()
        return super().get(request, *args, **kwargs)

    def save_data(self):
        self.forbid_non_specialist()
        super().save_data()
        # updates personal page's title
        if 'username' in self.user_form.changed_data:
            for page in SpecialistPage.objects.filter(user=self.request.user):
                page.save()


class SearchSpecialistsPagination(MultipleModelLimitOffsetPagination):
    default_limit = configurations.SEARCH_LIMIT


class SearchSpecialistsView(FlatMultipleModelAPIView):
    pagination_class = SearchSpecialistsPagination

    def get_querylist(self):
        query = self.request.GET.get('search')
        city = self.request.GET.get('city')
        querylist = [
            {
                'queryset': Profile.specialists.search(name=query, city=city),
                'serializer_class': SpecialistProfileSerializer
            }, {
                'queryset': Specialty.objects.search(name=query),
                'serializer_class': SpecialtySerializer
            }
        ]
        return querylist
