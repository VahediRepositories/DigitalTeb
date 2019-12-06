from modeltranslation.translator import register, TranslationOptions
from .articles.models import ArticleCategory


@register(ArticleCategory)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

