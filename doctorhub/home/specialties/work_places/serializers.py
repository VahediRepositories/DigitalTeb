from rest_framework import serializers
from .models import *


class WorkPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkPlace
        fields = [
            'id', 'medical_center',
            'city', 'name', 'website', 'address'
        ]


class WorkPlacePhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkPlacePhone
        fields = [
            'id', 'place', 'phone'
        ]
