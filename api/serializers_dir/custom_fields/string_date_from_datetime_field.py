from rest_framework import serializers


class StringDateFromDateTimeField(serializers.Field):

    def to_internal_value(self, data):
        pass

    def to_representation(self, value):
        return str(value.date())
