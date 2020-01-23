from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import *
from ...modules import pages


class WorkPlaceSerializer(serializers.ModelSerializer):

    page_url = SerializerMethodField()
    medical_center_name = SerializerMethodField()
    city_name = SerializerMethodField()
    image_url = SerializerMethodField()
    id = SerializerMethodField()

    def get_id(self, place):
        return f'place-{place.pk}'

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


class MedicalCenterSerializer(serializers.ModelSerializer):

    id = SerializerMethodField()
    page_url = SerializerMethodField()

    def get_page_url(self, medical_center):
        return pages.get_medical_center_page(medical_center).get_url()

    def get_id(self, medical_center):
        return f'medical-center-{medical_center.pk}'

    class Meta:
        model = MedicalCenter
        fields = [
            'id', 'plural_name', 'image_url', 'page_url'
        ]


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = [
            'place'
        ]

