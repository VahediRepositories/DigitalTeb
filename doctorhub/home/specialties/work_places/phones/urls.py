from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(
    'place-phones', views.WorkPlacePhoneViewSet, base_name='work-place-phones'
)

urlpatterns = [
    path(
        'create/<place_pk>/',
        views.PlacePhoneCreateView.as_view(),
        name='create_place_phone'
    ),
    path(
        'update/<pk>/',
        views.PlacePhoneUpdateView.as_view(),
        name='edit_place_phone',
    ),
    path('api/', include(router.urls))
]
