from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

from .. import configurations
from ..videos.blocks import MediaChooserBlock


class ImageParagraphBlock(blocks.StructBlock):
    image = ImageChooserBlock(help_text='high quality image')
    paragraph = blocks.RichTextBlock(
        features=configurations.RICHTEXT_FEATURES,
        help_text='It has to start with a farsi word'
    )


class VideoParagraphBlock(blocks.StructBlock):
    video = MediaChooserBlock(
        required=True, help_text='Choose an mp4 video'
    )
    paragraph = blocks.RichTextBlock(
        features=configurations.RICHTEXT_FEATURES,
        required=False,
        help_text='It has to start with a farsi word'
    )


class ImageCaptionBlock(blocks.StructBlock):
    image = ImageChooserBlock(help_text='high quality image')
    paragraph = blocks.RichTextBlock(
        features=configurations.RICHTEXT_FEATURES,
        required=False,
        help_text='It has to start with a farsi word'
    )


class ListBlock(blocks.StructBlock):
    paragraph = blocks.RichTextBlock(
        features=configurations.RICHTEXT_FEATURES,
        help_text='It has to start with a farsi word',
        required=False
    )
    items = blocks.ListBlock(
        blocks.RichTextBlock(
            features=configurations.RICHTEXT_FEATURES,
            help_text='It has to start with a farsi word',
        )
    )


class SectionBlock(blocks.StructBlock):
    title = blocks.RichTextBlock(
        features=[],
        required=False,
        help_text='It has to start with a farsi word'
    )
    content = blocks.StreamBlock(
        [
            ('text', blocks.RichTextBlock(
                features=configurations.RICHTEXT_FEATURES,
                icon='doc-full',
                help_text='It has to start with a farsi word'
            )),
            ('UL', ListBlock(icon='list-ul')),
            ('OL', ListBlock(icon='list-ol')),
            ('image_and_text_row', ImageParagraphBlock(icon='horizontalrule')),
            ('image', ImageCaptionBlock(icon='image')),
            ('video', VideoParagraphBlock(icon='media')),
        ], icon='cogs',
    )
