from rest_framework import serializers

from .models import *


class SymptomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Symptom
        fields = [
            'id', 'name', 'description',
        ]
