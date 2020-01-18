from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .models import *
from .specialties.models import *
from .specialties.work_places.models import *


# @receiver(pre_delete, sender=User, dispatch_uid='delete_specialist_page')
# def delete_specialist_page(sender, instance, **kwargs):
#     specialist_pages = SpecialistPage.objects.filter(
#         user=instance
#     )
#     if specialist_pages:
#         specialist_pages[0].delete()


@receiver(pre_delete, sender=WorkPlace, dispatch_uid='delete_work_place_page')
def delete_work_place_page(sender, instance, **kwargs):
    work_place_pages = WorkPlacePage.objects.filter(
        place=instance
    )
    if work_place_pages:
        work_place_pages[0].delete()


@receiver(post_save, sender=Specialty, dispatch_uid='create_specialty_page')
def create_specialty_page(sender, instance, created, **kwargs):
    if not SpecialtyPage.objects.filter(specialty=instance).exists():
        new_page = SpecialtyPage(specialty=instance)
        parent_page = new_page.get_specialists_page()
        parent_page.add_child(instance=new_page)
        new_page.save()


@receiver(post_save, sender=City, dispatch_uid='create_specialists_in_city_page')
def create_specialists_in_city_page(sender, instance, created, **kwargs):
    if not SpecialistsInCityPage.objects.filter(city=instance).exists():
        new_page = SpecialistsInCityPage(city=instance)
        parent_page = new_page.get_specialists_page()
        parent_page.add_child(instance=new_page)
        new_page.save()


@receiver(post_save, sender=City, dispatch_uid='create_specialty_in_city_pages')
def create_specialty_in_city_pages(sender, instance, created, **kwargs):
    for specialty in Specialty.objects.all():
        specialty_page = SpecialtyPage.objects.get(specialty=specialty)
        if not specialty_page.get_children().type(SpecialtyInCityPage).exists():
            new_page = SpecialtyInCityPage(city=instance)
            specialty_page.add_child(instance=new_page)
            new_page.save()


@receiver(post_save, sender=ArticleCategory, dispatch_uid='create_articles_category_page')
def create_articles_category_page(sender, instance, created, **kwargs):
    if not ArticlesCategoryPage.objects.filter(category=instance).exists():
        new_page = ArticlesCategoryPage(category=instance)
        parent_page = new_page.get_blogs_page()
        parent_page.add_child(instance=new_page)
        new_page.save()

