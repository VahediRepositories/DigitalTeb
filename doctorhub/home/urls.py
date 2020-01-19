from django.conf.urls import include
from django.urls import path
from wagtail.core import urls as wagtail_urls

from .accounts import urls as accounts_urls
from .articles import urls as articles_urls
from .specialties import urls as specialties_urls
from .locations import urls as locations_urls

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('accounts/', include(accounts_urls)),
    path('specialties/', include(specialties_urls)),
    path('articles/', include(articles_urls)),
    path('locations/', include(locations_urls)),
    path('', include(wagtail_urls)),
]


