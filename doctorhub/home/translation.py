from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from .articles.models import ArticleCategory
from .specialties.models import Specialty


@register(ArticleCategory)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Specialty)
class SpecialtyTranslationOptions(TranslationOptions):
    fields = ('name', 'specialist_name')

