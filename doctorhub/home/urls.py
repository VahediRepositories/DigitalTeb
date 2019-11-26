from django.conf.urls import include, url
from wagtail.core import urls as wagtail_urls

from .accounts import urls as accounts_urls

urlpatterns = accounts_urls.urlpatterns + [
    url(r'', include(wagtail_urls)),
]


