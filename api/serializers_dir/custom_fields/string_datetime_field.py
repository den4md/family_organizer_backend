from rest_framework import serializers


class StringDatetimeField(serializers.Field):

    def to_internal_value(self, data):
        pass

    def to_representation(self, value):
        return value.strftime('%Y-%m-%d %H:%M')
