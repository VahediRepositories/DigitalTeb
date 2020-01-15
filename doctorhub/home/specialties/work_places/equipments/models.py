from ..models import *


class EquipmentDefaultIcon(SquareIcon):
    pass


class Equipment(SquareIcon, MultilingualModelMixin, models.Model):
    place = models.ForeignKey(WorkPlace, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField()
