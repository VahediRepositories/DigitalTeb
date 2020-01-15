from ..models import *


@register_snippet
class PhoneIcon(SquareIcon):
    pass


class WorkPlacePhone(models.Model):
    place = models.ForeignKey(WorkPlace, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=30)

    @staticmethod
    def get_default_icon():
        return PhoneIcon.objects.last()
