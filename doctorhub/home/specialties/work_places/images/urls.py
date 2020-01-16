from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(
    'place-images', views.PlaceImageViewSet, base_name='work-place-images'
)

urlpatterns = [
    path(
        'create/<place_pk>',
        views.PlaceImageCreateView.as_view(),
        name='create_place_image'
    ),
    path(
        'update/<pk>',
        views.PlaceImageUpdateView.as_view(),
        name='edit_place_image',
    ),
    path('api/', include(router.urls))
]
