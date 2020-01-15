from rest_framework import serializers

from .models import *


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = [
            'place', 'name', 'description'
        ]
