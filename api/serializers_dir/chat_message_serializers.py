from rest_framework import serializers

from api.models_dir import chat_message
from api.serializers_dir import file_serializers, user_serializers
from api.serializers_dir.custom_fields import string_datetime_field


class ChatMessageServSerializer(serializers.ModelSerializer):
    file = file_serializers.FileServSerializer(read_only=True)
    user_sender = user_serializers.UserServMiniSerializer(read_only=True)
    send_datetime = string_datetime_field.StringDatetimeField(read_only=True)

    class Meta:
        model = chat_message.ChatMessage
        fields = ['id', 'is_text', 'text', 'file', 'user_sender', 'send_datetime', 'is_read']
