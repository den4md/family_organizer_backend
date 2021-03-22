from rest_framework import serializers

from api.models_dir import user
from api.serializers_dir import base_serializer


class UserAppSerializer(base_serializer.BaseAppSerializer):
    class Meta:
        model = user.User

        required_fields = {'email', 'password_hash', 'last_name', 'first_name'}
        non_required_fields = {'image_file_id', 'color', 'is_geo_transmitting_permitted', 'is_notifying_permitted'}
        possible_fields = required_fields | non_required_fields
        non_serialized_fields = {'password_hash', 'image_file_id'}
        fields = list(possible_fields - non_serialized_fields)


class UserServSerializer(serializers.ModelSerializer):
    class Meta:
        model = user.User
        fields = ['id', 'email', 'last_name', 'first_name', 'image_file', 'color', 'is_geo_transmitting_permitted',
                  'is_notifying_permitted']


class UserServMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = user.User
        fields = ['id', 'last_name', 'first_name', 'color', 'image_file_thumb']
