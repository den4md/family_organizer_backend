from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from api.serializers_dir import chat_message_serializers


class ChatLastMessageField(serializers.Field):
    def to_internal_value(self, data):
        pass

    def get_attribute(self, instance):
        return instance

    def to_representation(self, value):
        try:
            return chat_message_serializers.ChatMessageServSerializer(
                value.chat_message_list.latest('send_datetime')).data
        except ObjectDoesNotExist:
            return None
