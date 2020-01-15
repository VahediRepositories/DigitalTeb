from django.urls import path, include

from . import views
from .work_places import urls as work_place_urls
from .services import urls as service_urls
from .education import urls as education_urls
from .articles import urls as article_urls
from .symptoms import urls as symptom_urls

urlpatterns = [
    path(
        'profile/',
        views.SpecialistProfileView.as_view(),
        name='specialist_profile'
    ),
    path(
        'signup/',
        views.SpecialistSignUpView.as_view(),
        name='specialist_signup'
    ),
    path(
        'edit/',
        views.SpecialistProfileUpdateView.as_view(),
        name='edit_specialist_account'
    ),
    path(
        'work-places/',
        include(work_place_urls)
    ),
    path(
        'services/', include(service_urls)
    ),
    path(
        'education/', include(education_urls)
    ),
    path(
        'articles/', include(article_urls)
    ),
    path(
        'symptoms/', include(symptom_urls)
    ),

]
