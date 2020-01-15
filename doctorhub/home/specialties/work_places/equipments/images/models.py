from ..models import *
from .....images.mixins import CompressingImageMixin


class EquipmentImage(CompressingImageMixin, models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='equipments_gallery', null=False, blank=False
    )

    @property
    def place(self):
        return self.equipment.place

    @property
    def image_url(self):
        return self.image.url

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.compress_image()
