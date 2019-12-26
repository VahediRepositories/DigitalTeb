from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from .articles.models import *
from .specialties.models import *


@register(ArticleCategory)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Specialty)
class SpecialtyTranslationOptions(TranslationOptions):
    fields = ('name', 'specialist_name')


@register(MedicalCenter)
class MedicalCenterTranslationOptions(TranslationOptions):
    fields = ('name', 'plural_name')


@register(City)
class CityTranslationOptions(TranslationOptions):
    fields = ('name', )
