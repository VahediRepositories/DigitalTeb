from django.views.generic import FormView
from rest_framework import viewsets

from .permissions import *
from .serializers import *
from ...accounts.mixins import LoginRequiredMixin
from ...permissions import *
from ...specialties.mixins import NonSpecialistForbiddenMixin
from ...specialties.permissions import *


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = ArticlePage.objects.all()
    serializer_class = ArticlePageSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsSpecialistOrReadOnly,
        IsOwnerOrReadOnly,
        IsDeleteOrReadOnly,
    ]


class SpecialistArticlesView(
    LoginRequiredMixin,
    NonSpecialistForbiddenMixin,
    MultilingualViewMixin, CheckPhoneVerifiedMixin, FormView
):
    form_class = ArticleCreationForm

    @property
    def template_name(self):
        return f'home/specialists/{self.language_direction}/articles.html'

    def form_valid(self, form):
        self.forbid_non_specialist()
        category = form.cleaned_data['category']
        # TODO: use reverse to get the url
        return HttpResponseRedirect(
            f'/admin/pages/add/home/articlepage/{category.articlescategorypage.pk}/'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = ArticlePage.objects.filter(
            owner=self.request.user
        )
        return context

    def get(self, request, *args, **kwargs):
        self.forbid_non_specialist()
        self.check_phone_verified(request)
        return super().get(request, *args, **kwargs)