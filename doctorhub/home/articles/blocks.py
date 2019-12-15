from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

from .. import configurations
from ..videos.blocks import MediaChooserBlock


class VideoCaptionBlock(blocks.StructBlock):
    video = MediaChooserBlock(
        required=True, help_text='Choose an mp4 video'
    )
    paragraph = blocks.RichTextBlock(
        features=configurations.RICHTEXT_FEATURES,
        required=False,
    )


class ImageCaptionBlock(blocks.StructBlock):
    image = ImageChooserBlock(help_text='high quality image')
    paragraph = blocks.RichTextBlock(
        features=configurations.RICHTEXT_FEATURES,
        required=False,
    )


class SectionBlock(blocks.StructBlock):
    title = blocks.RichTextBlock(
        features=[],
        required=False,
    )
    content = blocks.StreamBlock(
        [
            (
                'text', blocks.RichTextBlock(
                    features=configurations.RICHTEXT_FEATURES,
                    icon='doc-full',
                )
            ),
            ('image', ImageCaptionBlock(icon='image')),
            ('video', VideoCaptionBlock(icon='media')),
        ], icon='cogs',
    )
