from rest_framework import serializers

from api.models_dir import event
from api.serializers_dir import base_app_serializer, file_serializers, user_serializers, map_point_serializers
from api.serializers_dir.custom_fields import string_datetime_field


class EventAppSerializer(base_app_serializer.BaseAppSerializer):
    class Meta:
        model = event.Event
        required_fields = {'event_datetime', 'name'}
        non_required_fields = {'description', 'file_id_list', 'map_point_id', 'notify_datetime'}
        possible_fields = required_fields | non_required_fields
        non_serialized_fields = {'file_id_list', 'map_point_id'}
        fields = list(possible_fields - non_serialized_fields)


class EventServSerializer(serializers.ModelSerializer):
    event_datetime = string_datetime_field.StringDatetimeField()
    file_list = file_serializers.FileServSerializer(many=True, read_only=True)
    map_point = map_point_serializers.MapPointServMiniSerializer(read_only=True)
    notify_datetime = string_datetime_field.StringDatetimeField()
    user_creator = user_serializers.UserServMiniSerializer()

    class Meta:
        model = event.Event
        fields = ['id', 'event_datetime', 'name', 'description', 'file_list', 'map_point', 'notify_datetime',
                  'create_date', 'user_creator']


class EventServMiniSerializer(serializers.ModelSerializer):
    event_datetime = string_datetime_field.StringDatetimeField()
    map_point = map_point_serializers.MapPointServMiniSerializer(read_only=True)
    notify_datetime = string_datetime_field.StringDatetimeField()

    class Meta:
        model = event.Event
        fields = ['id', 'event_datetime', 'name', 'map_point', 'notify_datetime']
