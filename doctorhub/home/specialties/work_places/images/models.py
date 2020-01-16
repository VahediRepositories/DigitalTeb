from ..models import *
from ....images.mixins import CompressingImageMixin


class WorkPlaceImage(CompressingImageMixin, models.Model):
    place = models.ForeignKey(WorkPlace, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='places_gallery', null=False, blank=False
    )

    @property
    def image_url(self):
        return self.image.url

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.compress_image()
