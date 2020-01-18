from django.conf.urls import include
from django.urls import path

from .cities import urls as cities_urls

urlpatterns = [
    path('cities/', include(cities_urls)),
]
