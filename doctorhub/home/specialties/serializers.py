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
