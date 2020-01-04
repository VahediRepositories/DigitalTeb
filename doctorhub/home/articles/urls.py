from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(
    r'article-page-comments', views.ArticlePageCommentViewSet, base_name='article-page-comments'
)

urlpatterns = [

    path(
        'articles/comment/',
        views.ArticlePageCommentCreateView.as_view(),
        name='article_page_create_comment'
    ),
    path('articles/api/', include(router.urls))

]
