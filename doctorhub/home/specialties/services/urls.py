from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(
    'services', views.ServiceViewSet, base_name='specialists-services'
)


urlpatterns = [

    path(
        'create/',
        views.ServiceCreateView.as_view(),
        name='create_service'
    ),
    path(
        'update/<pk>/',
        views.ServiceUpdateView.as_view(),
        name='edit_service'
    ),
    path('api/', include(router.urls))

]
