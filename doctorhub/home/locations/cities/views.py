from rest_framework.generics import ListAPIView

from ...locations.cities.serializers import *


class CitiesSearchView(ListAPIView):
    serializer_class = CitySerializer

    def get_queryset(self):
        return City.objects.search(
            name=self.request.GET.get('search', '')
        )

