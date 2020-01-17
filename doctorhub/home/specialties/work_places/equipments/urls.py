from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(
    'equipments', views.EquipmentViewSet, base_name='place-equipments'
)


urlpatterns = [

    path(
        'create/<place_pk>/',
        views.EquipmentCreateView.as_view(),
        name='create_equipment'
    ),
    path(
        'update/<pk>/',
        views.EquipmentUpdateView.as_view(),
        name='edit_equipment'
    ),
    path('api/', include(router.urls)),

]

