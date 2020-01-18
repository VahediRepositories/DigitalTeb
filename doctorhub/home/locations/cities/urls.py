from django.urls import path
from . import views

urlpatterns = [
    path(
        'search/', views.CitiesSearchView.as_view(), name='cities-search'
    ),
]
