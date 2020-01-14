from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(
    'education', views.EducationViewSet, base_name='specialists-education'
)


urlpatterns = [

    path(
        '',
        views.EducationCreateView.as_view(),
        name='create_education'
    ),
    path(
        'update/<pk>/',
        views.EducationUpdateView.as_view(),
        name='edit_education'
    ),
    path('api/', include(router.urls))

]
