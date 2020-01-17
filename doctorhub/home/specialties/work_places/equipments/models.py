from ..models import *
from ....images.mixins import SquareIconMixin


@register_snippet
class EquipmentDefaultIcon(SquareIcon):
    pass


class Equipment(MultilingualModelMixin, SquareIconMixin, models.Model):
    place = models.ForeignKey(WorkPlace, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(
        upload_to='equipment_images', null=True, blank=True
    )

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        else:
            return self.get_default_icon().image_url

    @staticmethod
    def get_default_icon():
        return EquipmentDefaultIcon.objects.last()

    def save(self, *args, **kwargs):
        self.set_multilingual_fields(
            ['name', 'description']
        )
        super().save(*args, **kwargs)
        self.make_square_image()
        self.compress_image()
