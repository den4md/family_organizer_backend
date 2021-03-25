from rest_framework import serializers


class StorageSizeField(serializers.Field):
    measures = ['b', 'Kb', 'Mb', 'Gb', 'Tb']

    def to_internal_value(self, data):
        pass

    def to_representation(self, value):
        for measure in self.measures:
            if value >= 1024:
                value = value // 1024
            else:
                break

        # noinspection PyUnboundLocalVariable
        return f'{value} {measure}'
