from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .phones import urls as phone_urls
from .images import urls as image_urls
from .equipments import urls as equipment_urls

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
        'cities/search/', views.CitiesSearchView.as_view(), name='cities-search'
    ),

    path(
        'phones/', include(phone_urls)
    ),
    path(
        'equipments/', include(equipment_urls)
    ),
    path(
        'images/', include(image_urls)
    ),

    path('api/', include(router.urls))

]
