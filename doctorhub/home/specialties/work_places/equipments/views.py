from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from .serializers import *
from ..permissions import IsPlaceStaffOrReadOnly


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [
        IsPlaceStaffOrReadOnly,
    ]

    def perform_create(self, serializer):
        place = serializer.validated_data['place']
        if place.has_staff(self.request.user):
            return super().perform_create(serializer)
        else:
            raise ValidationError(translation.gettext('Non-staff users cannot add equipment.'))

    def perform_update(self, serializer):
        place = serializer.validated_data['place']
        if place.has_staff(self.request.user):
            return super().perform_update(serializer)
        else:
            raise ValidationError(translation.gettext('Non-staff users cannot add equipment.'))
