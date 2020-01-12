from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(
    'symptoms', views.SymptomViewSet, base_name='specialists-symptoms'
)


urlpatterns = [

    path(
        '',
        views.SpecialistSymptomsView.as_view(),
        name='edit_symptoms'
    ),
    path(
        'update/<pk>/',
        views.SymptomUpdateView.as_view(),
        name='edit_symptom'
    ),
    path('api/', include(router.urls))

]
