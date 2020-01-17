from ...specialties.work_places.phones.models import *
from ...specialties.work_places.images.models import *
from ...specialties.work_places.equipments.models import *
from .. import images


def save_place_image(place, image_data):
    try:
        file_name = f'{place.name}'

        def save_image(file_path, content_file):
            place.image.save(
                file_path, content_file, save=True
            )

        images.save_base64_to_file(file_name, image_data, save_image)
    except Exception as e:
        import traceback
        traceback.print_exc()


def get_default_work_place():
    return WorkPlace.objects.first()


def get_place_phones(place):
    return WorkPlacePhone.objects.filter(place=place)


def get_place_equipments(place):
    return Equipment.objects.filter(place=place)


def get_place_images(place):
    return WorkPlaceImage.objects.filter(place=place)
