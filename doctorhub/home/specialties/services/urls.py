from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(
    'services', views.ServiceViewSet, base_name='specialists-services'
)


urlpatterns = [

    path(
        '',
        views.SpecialistServicesView.as_view(),
        name='edit_services'
    ),
    path(
        'update/<pk>/',
        views.ServiceUpdateView.as_view(),
        name='edit_service'
    ),
    path('api/', include(router.urls))

]
