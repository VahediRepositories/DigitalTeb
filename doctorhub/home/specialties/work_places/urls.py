from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(
    'work-places/phones', views.WorkPlacePhoneViewSet, base_name='work-place-phones'
)
router.register(
    'work-places', views.WorkPlaceViewSet, base_name='specialists-work-places'
)


urlpatterns = [
    path(
        '',
        views.SpecialistWorkPlacesView.as_view(),
        name='edit_work_places'
    ),
    path(
        'update/<pk>/',
        views.SpecialistWorkPlaceUpdateView.as_view(),
        name='edit_work_place'
    ),
    path('api/', include(router.urls))
]
