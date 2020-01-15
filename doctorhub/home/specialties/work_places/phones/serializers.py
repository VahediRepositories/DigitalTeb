from rest_framework import serializers
from .models import WorkPlacePhone


class WorkPlacePhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkPlacePhone
        fields = [
            'id', 'place', 'phone_number'
        ]
