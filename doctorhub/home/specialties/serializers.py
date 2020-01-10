from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import *
from .work_places.models import *
from ..modules import pages


class WorkPlaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkPlace
        fields = [
            'id', 'medical_center',
            'city', 'name', 'website', 'address'
        ]


class SpecialtySerializer(serializers.ModelSerializer):

    id = SerializerMethodField()
    image_url = SerializerMethodField()
    page_url = SerializerMethodField()

    def get_page_url(self, specialty):
        return pages.get_specialty_page(specialty).get_url()

    def get_image_url(self, specialty):
        return specialty.image.get_rendition('fill-512x512').url

    def get_id(self, specialty):
        return f'specialty-{specialty.pk}'

    class Meta:
        model = Specialty
        fields = [
            'id', 'name', 'image_url', 'page_url'
        ]
