from rest_framework import serializers

from api.models_dir import file
from api.serializers_dir import user_serializers
from api.serializers_dir.custom_fields.string_datetime_field import StringDatetimeField


class FileServSerializer(serializers.ModelSerializer):
    upload_datetime = StringDatetimeField()
    user_uploader = user_serializers.UserServMiniSerializer(read_only=True)

    class Meta:
        model = file.File
        fields = ['id', 'name', 'type', 'size', 'upload_datetime', 'user_uploader']
