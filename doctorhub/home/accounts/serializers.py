from rest_framework import serializers

from .models import *


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = [
            'name', 'image_url'
        ]
