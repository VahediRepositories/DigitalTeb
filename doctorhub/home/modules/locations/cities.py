from django.shortcuts import get_object_or_404

from ...locations.cities.models import *


def get_city_from_request(request):
    city = request.GET.get('city', '')
    if city:
        return get_object_or_404(City, name=city)
    else:
        return None
