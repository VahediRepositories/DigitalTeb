from django.urls import path

from . import views

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

]
