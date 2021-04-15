from rest_framework import serializers

from api.models_dir import user_map_point
from api.serializers_dir import base_app_serializer, user_serializers
from api.serializers_dir.custom_fields import string_datetime_field


class UserMapPointAppSerializer(base_app_serializer.BaseAppSerializer):
    class Meta:
        model = user_map_point.UserMapPoint
        possible_fields = required_fields = {'latitude', 'longitude'}
        fields = list(possible_fields)


class UserMapPointServSerializer(serializers.ModelSerializer):
    user = user_serializers.UserServMiniSerializer(read_only=True)
    datetime = string_datetime_field.StringDatetimeField(read_only=True)

    class Meta:
        model = user_map_point.UserMapPoint
        fields = ['user', 'latitude', 'longitude', 'datetime']
