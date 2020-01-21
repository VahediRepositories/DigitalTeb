from rest_framework import serializers
from .models import *


class WeekDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = WeekDay
        fields = [
            'id', 'place', 'user', 'days'
        ]
