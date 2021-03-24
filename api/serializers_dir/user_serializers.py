from rest_framework import serializers

from api.models_dir import user
from api.serializers_dir import base_app_serializer
from api.serializers_dir.custom_fields import string_date_from_datetime_field


class UserAppSerializer(base_app_serializer.BaseAppSerializer):
    class Meta:
        model = user.User

        required_fields = {'email', 'password_hash', 'last_name', 'first_name'}
        non_required_fields = {'image_file_id', 'color', 'is_geo_transmitting_permitted', 'is_notifying_permitted'}
        possible_fields = required_fields | non_required_fields
        non_serialized_fields = {'password_hash', 'image_file_id'}
        fields = list(possible_fields - non_serialized_fields)


class UserServMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = user.User
        fields = ['id', 'last_name', 'first_name', 'color', 'image_file_thumb']


from api.serializers_dir import file_serializers


class UserServSerializer(serializers.ModelSerializer):
    image_file = file_serializers.FileServSerializer(read_only=True)
    date_joined = string_date_from_datetime_field.StringDateFromDateTimeField()

    class Meta:
        model = user.User
        fields = ['id', 'email', 'last_name', 'first_name', 'image_file', 'color', 'is_geo_transmitting_permitted',
                  'is_notifying_permitted', 'date_joined']
