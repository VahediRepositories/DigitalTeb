from rest_framework import serializers
from .models import *


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = [
            'id', 'name', 'description'
        ]
