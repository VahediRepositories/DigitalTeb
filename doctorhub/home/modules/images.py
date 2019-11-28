import base64

from django.core.files.base import ContentFile


def save_base64_to_file(file_name, data, save_file):
    file_format, img_str = data.split(';base64,')
    ext = file_format.split('/')[-1]
    content_file = ContentFile(base64.b64decode(img_str))
    save_file(f'{file_name}.{ext}', content_file)
