from drf_multiple_model.pagination import MultipleModelLimitOffsetPagination
from drf_multiple_model.views import FlatMultipleModelAPIView
from .accounts.models import Profile
from .accounts.serializers import SpecialistProfileSerializer
from . import configurations


class SearchPagination(MultipleModelLimitOffsetPagination):
    default_limit = configurations.SEARCH_LIMIT


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
