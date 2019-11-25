from django.conf.urls import include, url
from wagtail.core import urls as wagtail_urls

from .authentication import urls as auth_urls

urlpatterns = auth_urls.urlpatterns + [
    url(r'', include(wagtail_urls)),
]


