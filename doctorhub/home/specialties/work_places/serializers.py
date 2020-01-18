from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import *


class WorkPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkPlace
        fields = [
            'id', 'medical_center',
            'city', 'name', 'website', 'address'
        ]


class CitySerializer(serializers.ModelSerializer):

    id = SerializerMethodField()
    text = SerializerMethodField()

    def get_id(self, city):
        return self.get_text(city)

    def get_text(self, city):
        return city.name

    class Meta:
        model = City
        fields = [
            'id', 'name', 'text'
        ]
