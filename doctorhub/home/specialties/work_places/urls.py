from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .phones import urls as phone_urls
from .images import urls as image_urls

router = DefaultRouter()
router.register(
    'work-places', views.WorkPlaceViewSet, base_name='specialists-work-places'
)


urlpatterns = [
    path(
        'create/',
        views.WorkPlaceCreateView.as_view(),
        name='create_work_place'
    ),
    path(
        'profile/<pk>/',
        views.WorkPlaceView.as_view(),
        name='work_place_profile'
    ),
    path(
        'update/<pk>/',
        views.WorkPlaceUpdateView.as_view(),
        name='edit_work_place'
    ),
    path(
        'phones/', include(phone_urls)
    ),
    path(
        'images/', include(image_urls)
    ),

    path('api/', include(router.urls))
]
