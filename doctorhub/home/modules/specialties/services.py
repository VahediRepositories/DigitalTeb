from ...specialties.services.models import *
from .. import text_processing
from .. import images


def save_service_image(service, image_data):
    try:
        file_name = f'{service.name}'

        def save_image(file_path, content_file):
            service.image.save(
                file_path, content_file, save=True
            )

        images.save_base64_to_file(file_name, image_data, save_image)
    except Exception as e:
        import traceback
        traceback.print_exc()


def get_user_services(user):
    return Label.objects.filter(owner=user)


def get_user_services_str(user):
    labels = get_user_services(user)
    return text_processing.str_list_to_comma_separated(
        [
            label.name for label in labels
        ]
    )
