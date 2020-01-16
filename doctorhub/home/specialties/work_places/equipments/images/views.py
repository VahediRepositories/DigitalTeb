from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from .serializers import *
from ...permissions import IsPlaceStaffOrReadOnly


class EquipmentImageViewSet(viewsets.ModelViewSet):

    queryset = EquipmentImage.objects.all()
    serializer_class = EquipmentImageSerializer
    permission_classes = [
        IsPlaceStaffOrReadOnly,
    ]

    def perform_create(self, serializer):
        equipment = serializer.validated_data['equipment']
        place = equipment.place
        if place.has_staff(self.request.user):
            return super().perform_create(serializer)
        else:
            raise ValidationError(translation.gettext('Non-staff users cannot add equipment image'))

    def perform_update(self, serializer):
        equipment = serializer.validated_data['equipment']
        place = equipment.place
        if place.has_staff(self.request.user):
            return super().perform_update(serializer)
        else:
            raise ValidationError(translation.gettext('Non-staff users cannot add equipment image'))
