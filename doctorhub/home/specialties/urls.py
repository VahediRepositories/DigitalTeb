from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(
    r'specialists-work-places', views.WorkPlaceViewSet, base_name='specialists-work-places'
)
router.register(
    r'specialists-profiles', views.SpecialistViewSet, base_name='specialists-profiles'
)

urlpatterns = [
    path(
        'specialists/profile/',
        views.SpecialistProfileView.as_view(),
        name='specialist_profile'
    ),
    path(
        'specialists/signup/',
        views.SpecialistSignUpView.as_view(),
        name='specialist_signup'
    ),
    path(
        'specialists/edit/',
        views.SpecialistProfileUpdateView.as_view(),
        name='edit_specialist_account'
    ),
    path(
        'specialists/technical-info/edit/',
        views.TechnicalInformationView.as_view(),
        name='edit_technical_info'
    ),
    path(
        'specialists/services/',
        views.SpecialistLabelsView.as_view(),
        name='edit_labels'
    ),
    path(
        'specialists/education/',
        views.SpecialistEducationView.as_view(),
        name='edit_education'
    ),
    path(
        'specialists/articles/',
        views.SpecialistArticlesView.as_view(),
        name='specialist_articles'
    ),
    path(
        'specialists/biography/<pk>/',
        views.BiographyView.as_view(),
        name='edit_biography'
    ),
    path(
        'specialists/work-places/',
        views.SpecialistWorkPlacesView.as_view(),
        name='edit_work_places'
    ),
    path(
        'specialists/work-places/<pk>/',
        views.SpecialistWorkPlaceUpdateView.as_view(),
        name='edit_work_place'
    ),
    path('specialists/api/', include(router.urls))

]
