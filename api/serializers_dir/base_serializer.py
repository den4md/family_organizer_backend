from rest_framework import serializers


class BaseSerializer(serializers.ModelSerializer):

    def __init__(self, **kwargs):
        if type(self) != BaseSerializer:
            super().__init__(**kwargs)
        else:
            raise TypeError('Can\'t initialize abstract class \'BaseSerializer\'')

    class Meta:
        required_fields = {}
        possible_fields = {}
