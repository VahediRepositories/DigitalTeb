from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(
    'week-days', views.WeekDayViewSet, base_name='week-days'
)
router.register(
    'work-times', views.WorkTimeViewSet, base_name='work-times'
)

urlpatterns = [
    path(
        'week-days/create/<place_pk>/',
        views.WeekDayCreateView.as_view(),
        name='create_week_day'
    ),
    path(
        'work-times/create/<day_pk>/',
        views.WorkTimeCreateView.as_view(),
        name='create_work_time'
    ),
    path(
        'week-days/<pk>/',
        views.WeekDayView.as_view(),
        name='week-day'
    ),
    path('api/', include(router.urls))
]
