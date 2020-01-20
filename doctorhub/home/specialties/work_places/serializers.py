from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import *
from ...modules import pages


class WorkPlaceSerializer(serializers.ModelSerializer):

    page_url = SerializerMethodField()
    medical_center_name = SerializerMethodField()
    city_name = SerializerMethodField()
    image_url = SerializerMethodField()

    def get_image_url(self, place):
        return place.image_url

    def get_city_name(self, place):
        return place.city.name

    def get_page_url(self, place):
        return pages.get_work_place_page(place).get_url()

    def get_medical_center_name(self, place):
        return place.medical_center.name

    class Meta:
        model = WorkPlace
        fields = [
            'id', 'medical_center',
            'city', 'name', 'address',
            'page_url', 'medical_center_name',
            'city_name', 'image_url',
        ]
