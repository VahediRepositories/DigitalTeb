from rest_framework import serializers

from .models import *


class PlaceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkPlaceImage
        fields = ['place']
