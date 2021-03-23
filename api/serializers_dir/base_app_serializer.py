from rest_framework import serializers


class BaseAppSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        if type(self) != BaseAppSerializer:
            super().__init__(*args, **kwargs)
        else:
            raise TypeError('Can\'t initialize abstract class \'BaseSerializer\'')

    class Meta:
        required_fields = {}
        non_required_fields = {}
        possible_fields = {}
        non_serialized_fields = {}
        fields = []
