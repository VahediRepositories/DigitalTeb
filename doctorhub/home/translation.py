from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from .articles.models import ArticleCategory


@register(ArticleCategory)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

