from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel


class Category(models.Model):
    farsi_name = models.TextField()
    english_name = models.TextField()
    horizontal_image = models.ForeignKey(
        'wagtailimages.Image',
        help_text='high quality horizontal image',
        null=True, blank=False, on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('farsi_name'),
        FieldPanel('english_name'),
        ImageChooserPanel('horizontal_image')
    ]

    def __str__(self):
        return self.farsi_name

    class Meta:
        abstract = True
