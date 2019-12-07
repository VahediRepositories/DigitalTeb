from django.forms import TextInput
from django.utils import translation
from django.conf import settings
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldRowPanel, FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet

from ..categories.models import *


@register_snippet
class ArticleCategory(Category):

    horizontal_image = models.ForeignKey(
        'wagtailimages.Image',
        help_text='high quality horizontal image',
        null=True, blank=False, on_delete=models.SET_NULL, related_name='+'
    )
    square_image = models.ForeignKey(
        'wagtailimages.Image',
        help_text='high quality square image',
        null=True, blank=False, on_delete=models.SET_NULL, related_name='+'
    )

    @property
    def default_name(self):
        current = translation.get_language()
        translation.activate(settings.LANGUAGE_CODE)
        name = self.name
        translation.activate(current)
        return name

    @property
    def icon(self):
        if self.square_image:
            return self.square_image
        else:
            return self.horizontal_image

    panels = [
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                         FieldPanel('name_en_us', widget=TextInput),
                         FieldPanel('name_fa_ir', widget=TextInput),
                    ]
                ),
            ], heading='Name', classname="collapsible collapsed"
        ),
        MultiFieldPanel(
            [
                ImageChooserPanel('horizontal_image'),
                ImageChooserPanel('square_image'),
            ], heading='Image', classname="collapsible collapsed"
        )
    ]

    class Meta:
        verbose_name_plural = "Article Categories"



