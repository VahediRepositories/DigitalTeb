from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .phones import urls as phone_urls
from .images import urls as image_urls
from .equipments import urls as equipment_urls
from .times import urls as time_urls

router = DefaultRouter()
router.register(
    'work-places', views.WorkPlaceViewSet, base_name='specialists-work-places'
)
router.register(
    'memberships', views.MembershipViewSet, base_name='memberships'
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
        'search/',
        views.SearchMedicalCentersView.as_view(),
        name='medical-centers-search'
    ),
    path(
        'accept-membership/',
        views.AcceptMembershipView.as_view(),
        name='memberships-accept'
    ),
    path(
        'reject-membership/',
        views.RejectMembershipView.as_view(),
        name='memberships-reject'
    ),
    path(
        'cancel-membership/',
        views.CancelMembershipView.as_view(),
        name='membership-cancel'
    ),
    path(
        'times/', include(time_urls)
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
