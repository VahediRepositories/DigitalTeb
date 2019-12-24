from django import forms
from django.utils import translation

from ..articles.models import ArticleCategory, ArticlePageComment


class ArticleCreationForm(forms.Form):

    category = forms.ModelChoiceField(
        label=translation.gettext_lazy('Category'),
        queryset=ArticleCategory.objects.all()
    )


class ArticlePageCommentForm(forms.ModelForm):
    class Meta:
        model = ArticlePageComment
        fields = [
            'comment'
        ]



