from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(
    r'comments', views.ArticlePageCommentViewSet, base_name='article-page-comments'
)

urlpatterns = [

    path(
        'comments/',
        views.ArticlePageCommentCreateView.as_view(),
        name='article_page_create_comment'
    ),
    path('api/', include(router.urls))

]
