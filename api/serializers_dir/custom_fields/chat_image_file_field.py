from rest_framework import serializers

from api.serializers_dir import file_serializers


class ChatImageFileField(serializers.Field):
    def to_internal_value(self, data):
        pass

    def get_attribute(self, instance):
        return instance

    def to_representation(self, value):
        if value.is_main_group_chat:
            if value.group.image_file is None:
                return None
            else:
                return file_serializers.FileServSerializer(value.group.image_file).data
        elif not value.is_group_chat:
            return file_serializers.FileServSerializer(
                value.user_member_list.exclude(id=self.context['request_user_id']).get().image_file).data
        else:
            return None
