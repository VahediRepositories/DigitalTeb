from rest_framework import serializers

from .models import *


class WorkPlaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkPlace
        fields = [
            'id', 'medical_center',
            'city', 'name', 'website', 'address'
        ]

    def validate(self, data):
        return super().validate(data)
        # parent = data['parent']
        # if parent:
        #     if parent.article != data['article']:
        #         raise serializers.ValidationError(
        #             translation.gettext("Comment's article and it's parent's article are different")
        #         )
        # if self.instance:
        #     if self.instance.article != data['article']:
        #         raise serializers.ValidationError(
        #             translation.gettext("Comment's article can not be changed")
        #         )
        # return data
