from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import *
from ..modules import pages, text_processing
from ..modules.specialties import services as services_module


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = [
            'name', 'image_url'
        ]


class SpecialistProfileSerializer(ProfileSerializer):

    page_url = SerializerMethodField()
    id = SerializerMethodField()
    services = SerializerMethodField()

    def get_services(self, profile):
        services = services_module.get_user_services_str(profile.user)
        return text_processing.truncatechars(services, 300)

    def get_page_url(self, profile):
        return pages.get_specialist_page(profile.user).get_url()

    def get_id(self, profile):
        return f'profile-{profile.pk}'

    class Meta(ProfileSerializer.Meta):
        fields = ProfileSerializer.Meta.fields + [
            'id', 'page_url', 'services'
        ]
