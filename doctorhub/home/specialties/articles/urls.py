from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(
    'articles', views.ArticleViewSet, base_name='specialists-articles'
)

urlpatterns = [
    path('', views.SpecialistArticlesView.as_view(), name='edit_articles'),
    path('api/', include(router.urls))
]
