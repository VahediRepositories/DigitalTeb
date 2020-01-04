from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import *
from ..accounts.serializers import ProfileSerializer
from ..modules import pages


class WorkPlaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkPlace
        fields = [
            'id', 'medical_center',
            'city', 'name', 'website', 'address'
        ]


class SpecialistProfileSerializer(ProfileSerializer):

    page_url = SerializerMethodField()

    def get_page_url(self, profile):
        return pages.get_specialist_page(profile.user).get_url()

    class Meta(ProfileSerializer.Meta):
        fields = ProfileSerializer.Meta.fields + [
            'page_url'
        ]

