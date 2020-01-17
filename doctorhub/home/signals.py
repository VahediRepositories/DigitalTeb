from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import SpecialtyPage
from .specialties.models import Specialty


# @receiver(pre_delete, sender=User, dispatch_uid='delete_specialist_page')
# def delete_specialist_page(sender, instance, **kwargs):
#     specialist_pages = SpecialistPage.objects.filter(
#         user=instance
#     )
#     if specialist_pages:
#         specialist_pages[0].delete()


@receiver(post_save, sender=Specialty, dispatch_uid='create_specialty_page')
def create_specialty_page(sender, instance, created, **kwargs):
    if not SpecialtyPage.objects.filter(specialty=instance).exists():
        new_page = SpecialtyPage(specialty=instance)
        parent_page = new_page.get_specialists_page()
        parent_page.add_child(instance=new_page)
        new_page.save()
