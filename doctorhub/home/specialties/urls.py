from django.urls import path

from . import views

urlpatterns = [

    path(
        'specialists/personal_page/<pk>/',
        views.PersonalPageView.as_view(),
        name='personal_page'
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
        'specialists/labels',
        views.SpecialistLabelsView.as_view(),
        name='edit_labels'
    ),
    path(
        'specialists/biography/<pk>/',
        views.BiographyView.as_view(),
        name='edit_biography'
    ),

]
