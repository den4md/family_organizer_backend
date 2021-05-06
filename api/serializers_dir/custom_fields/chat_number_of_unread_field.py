from rest_framework import serializers

from api.serializers_dir import file_serializers


class ChatNumberOfUnreadField(serializers.Field):
    def to_internal_value(self, data):
        pass

    def get_attribute(self, instance):
        return instance

    def to_representation(self, value):
        return value.chat_user_settings.get(user__id=self.context['request_user_id']).number_of_unread_messages
