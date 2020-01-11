from rest_framework import serializers
from .models import *


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = [
            'id', 'level', 'field', 'institution'
        ]
