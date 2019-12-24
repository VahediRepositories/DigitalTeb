from django.conf.urls import include, url
from django.urls import path
from wagtail.core import urls as wagtail_urls

from .accounts import urls as accounts_urls
from .articles import urls as articles_urls
from .specialties import urls as specialties_urls

urlpatterns = [
    path('api-auth/', include('rest_framework.urls'))
]
urlpatterns += accounts_urls.urlpatterns + specialties_urls.urlpatterns + articles_urls.urlpatterns
urlpatterns += [
    url(r'', include(wagtail_urls)),
]


