from django.db import models
from wagtail.admin.edit_handlers import MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel


class SquareIcon(models.Model):
    image = models.ForeignKey(
        'wagtailimages.Image',
        help_text='high quality square image',
        null=True, blank=False, on_delete=models.PROTECT, related_name='+'
    )

    @property
    def image_url(self):
        return self.image.get_rendition('fill-512x512').url

    panels = [
        MultiFieldPanel(
            [
               ImageChooserPanel('image')
            ], heading='Image', classname="collapsible collapsed"
        ),
    ]

    class Meta:
        abstract = True
