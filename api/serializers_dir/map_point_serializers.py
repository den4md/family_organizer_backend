from rest_framework import serializers

from api.models_dir import map_point
from api.serializers_dir import base_app_serializer, file_serializers, user_serializers


class MapPointAppSerializer(base_app_serializer.BaseAppSerializer):
    class Meta:
        model = map_point.MapPoint
        required_fields = {'name', 'latitude', 'longitude'}
        non_required_fields = {'description', 'image_file_id'}
        possible_fields = required_fields | non_required_fields
        non_serialized_fields = {'image_file_id'}
        fields = list(possible_fields - non_serialized_fields)


class MapPointServMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = map_point.MapPoint
        fields = ['id', 'name', 'image_file_thumb', 'latitude', 'longitude']


from api.serializers_dir import event_serializers


class MapPointServSerializer(serializers.ModelSerializer):
    image_file = file_serializers.FileServSerializer(read_only=True)
    event_list = event_serializers.EventServMiniSerializer(many=True, read_only=True)
    user_creator = user_serializers.UserServMiniSerializer(read_only=True)

    class Meta:
        model = map_point.MapPoint
        fields = ['id', 'name', 'description', 'image_file', 'latitude', 'longitude', 'event_list', 'create_date',
                  'user_creator']
