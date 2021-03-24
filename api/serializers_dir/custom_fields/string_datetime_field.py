from rest_framework import serializers


# TODO Delete if unused
class StringDatetimeField(serializers.Field):

    def to_internal_value(self, data):
        pass

    def to_representation(self, value):
        return value.strfdate.strftime('%Y-%m-%d %H:%M')
