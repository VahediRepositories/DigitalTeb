from rest_framework import serializers

from .models import *


class EquipmentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentImage
        fields = ['equipment']
