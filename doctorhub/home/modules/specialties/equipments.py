from .. import images
from ...specialties.work_places.equipments.models import *
from .. import text_processing


def save_equipment_image(equipment, image_data):
    try:
        file_name = f'{equipment.name}'

        def save_image(file_path, content_file):
            equipment.image.save(
                file_path, content_file, save=True
            )

        images.save_base64_to_file(file_name, image_data, save_image)
    except Exception as e:
        import traceback
        traceback.print_exc()


def get_place_equipments(place):
    return Equipment.objects.filter(place=place)


def get_place_equipments_str(place):
    equipments = get_place_equipments(place)
    return text_processing.str_list_to_comma_separated(
        [
            equipment.name for equipment in equipments
        ]
    )
