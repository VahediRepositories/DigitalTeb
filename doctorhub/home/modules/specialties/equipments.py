from .. import images


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
