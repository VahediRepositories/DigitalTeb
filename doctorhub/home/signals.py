from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .models import *
from .specialties.models import *
from .specialties.work_places.models import *


@receiver(pre_delete, sender=WorkPlace, dispatch_uid='delete_work_place_page')
def delete_work_place_page(sender, instance, **kwargs):
    work_place_pages = WorkPlacePage.objects.filter(
        place=instance
    )
    if work_place_pages:
        work_place_pages[0].delete()


@receiver(post_save, sender=ArticleCategory, dispatch_uid='category_saved')
def category_saved(sender, instance, created, **kwargs):
    blogs_page = DigitalTebPageMixin.get_blogs_page()
    blogs_page.update_tree()


@receiver(post_save, sender=Specialty, dispatch_uid='specialty_saved')
def specialty_saved(sender, instance, created, **kwargs):
    specialists_page = DigitalTebPageMixin.get_specialists_page()
    specialists_page.update_tree()


@receiver(post_save, sender=MedicalCenter, dispatch_uid='medical_center_saved')
def medical_center_saved(sender, instance, created, **kwargs):
    medical_centers_page = DigitalTebPageMixin.get_medical_centers_page()
    medical_centers_page.update_tree()


@receiver(post_save, sender=City, dispatch_uid='city_saved')
def city_saved(sender, instance, created, **kwargs):
    specialists_page = DigitalTebPageMixin.get_specialists_page()
    medical_centers_page = DigitalTebPageMixin.get_medical_centers_page()
    specialists_page.update_tree()
    medical_centers_page.update_tree()

