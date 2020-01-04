from drf_multiple_model.pagination import MultipleModelLimitOffsetPagination
from drf_multiple_model.views import FlatMultipleModelAPIView
from .accounts.models import Profile
from .specialties.serializers import SpecialistProfileSerializer


class SearchPagination(MultipleModelLimitOffsetPagination):
    default_limit = 10


class SearchView(FlatMultipleModelAPIView):
    pagination_class = SearchPagination

    def get_querylist(self):
        query = self.request.GET.get('search')
        querylist = [
            {
                'queryset': Profile.specialists.search(name=query),
                'serializer_class': SpecialistProfileSerializer
            }
        ]
        return querylist
