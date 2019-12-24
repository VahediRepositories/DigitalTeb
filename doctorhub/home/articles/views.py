from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.views.generic.edit import FormView
from rest_framework import viewsets, permissions

from .forms import ArticlePageCommentForm
from .serializers import *
from ..accounts.mixins import LoginRequiredMixin
from ..models import ArticlePage
from ..multilingual.mixins import MultilingualViewMixin
from ..permissions import IsOwnerOrReadOnly


class ArticlePageCommentCreateView(
    SuccessMessageMixin,
    LoginRequiredMixin,
    MultilingualViewMixin, FormView
):
    success_message = translation.gettext_lazy(
        'Your comment was saved'
    )
    form_class = ArticlePageCommentForm

    @property
    def template_name(self):
        return f'home/articles/article_page/comments/create/{self.language_direction}/create_comment.html'

    @property
    def article_page(self):
        return get_object_or_404(
            ArticlePage, pk=self.request.GET.get('article')
        )

    def get_success_url(self):
        return self.article_page.get_url()

    def form_valid(self, form):
        new_comment = ArticlePageComment.objects.create(
            owner=self.request.user, comment=form.cleaned_data['comment'],
            article=self.article_page
        )
        parent = self.request.GET.get('parent-id')
        if parent:
            parent = get_object_or_404(
                ArticlePageComment, pk=parent
            )
            new_comment.parent = parent
            new_comment.save()

        return super().form_valid(form)


class ArticlePageCommentViewSet(viewsets.ModelViewSet):
    queryset = ArticlePageComment.objects.all()
    serializer_class = ArticlePageCommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user,
        )



