from wagtail.images.models import Image

from ..models import *
from ....images.mixins import CompressingImageMixin


class WorkPlaceImage(CompressingImageMixin, models.Model):
    place = models.ForeignKey(WorkPlace, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='places_gallery', null=False, blank=False
    )
    wagtail_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True, on_delete=models.PROTECT, related_name='+'
    )

    @property
    def image_url(self):
        return self.wagtail_image.get_rendition('original').url

    def save(self, *args, **kwargs):
        self.wagtail_image = Image.objects.create(
            file=self.image.file, title=f'{self.place.name}'
        )
        super().save(*args, **kwargs)
        self.compress_image()
