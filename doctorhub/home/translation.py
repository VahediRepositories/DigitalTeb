from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from .accounts.models import *
from .articles.models import *
from .specialties.education.models import *
from .specialties.models import *
from .specialties.services.models import *
from .specialties.work_places.equipments.models import *


@register(Profile)
class ProfileTranslationOptions(TranslationOptions):
    fields = ('first_name', 'last_name',)


@register(Label)
class LabelTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)


@register(Symptom)
class SymptomTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)


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
    fields = ('name',)


@register(WorkPlace)
class WorkPlaceTranslationOptions(TranslationOptions):
    fields = ('name', 'address',)


@register(Education)
class EducationTranslationOptions(TranslationOptions):
    fields = ('level', 'field', 'institution')


@register(Equipment)
class EquipmentTranslationOptions(TranslationOptions):
    fields = ('name', 'description')
