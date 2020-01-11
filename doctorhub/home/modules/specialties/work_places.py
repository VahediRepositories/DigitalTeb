from ...specialties.work_places.models import *


def save_place_logo_image(place, image_data):
    try:
        file_name = f'{place.name}'

        def save_logo_image(file_path, content_file):
            place.logo_image.save(
                file_path, content_file, save=True
            )

        images.save_base64_to_file(file_name, image_data, save_logo_image)
    except Exception as e:
        import traceback
        traceback.print_exc()


def get_default_work_place():
    return WorkPlace.objects.first()
