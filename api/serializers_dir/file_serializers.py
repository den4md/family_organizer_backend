from rest_framework import serializers

from api.models_dir import file
from api.serializers_dir import user_serializers
from api.serializers_dir.custom_fields import storage_size_field
from api.serializers_dir.custom_fields import string_datetime_field


class FileServSerializer(serializers.ModelSerializer):
    upload_datetime = string_datetime_field.StringDatetimeField(read_only=True)
    user_uploader = user_serializers.UserServMiniSerializer(read_only=True)
    size = storage_size_field.StorageSizeField(read_only=True)

    class Meta:
        model = file.File
        fields = ['id', 'name', 'extension', 'size', 'upload_datetime', 'user_uploader']
