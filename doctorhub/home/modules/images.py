import base64

from PIL import Image
from django.core.files.base import ContentFile


def save_base64_to_file(file_name, data, save_file):
    file_format, img_str = data.split(';base64,')
    ext = file_format.split('/')[-1]
    content_file = ContentFile(base64.b64decode(img_str))
    save_file(f'{file_name}.{ext}', content_file)


def make_square_image(image_path):
    img = Image.open(image_path)
    if img.height != img.width:
        size = min(img.height, img.width)
        img = img.resize((size, size))
        img.save(image_path)


# def compress_image(image_path):
#     img = Image.open(image_path)
#     if img.height > 512 or img.width > 512:
#         output_size = (512, 512)
#         img = img.resize(output_size)
#         img.save(image_path)


def compress_image(image_path):
    img = Image.open(image_path)
    if img.height > 1024 or img.width > 1024:
        output_size = (
            int(img.width / 2), int(img.height / 2)
        )
        img = img.resize(output_size)
        img.save(image_path)
        compress_image(image_path)
