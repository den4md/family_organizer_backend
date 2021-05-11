from rest_framework import serializers

from api.models_dir import chat
from api.serializers_dir import user_serializers
from api.serializers_dir.custom_fields import chat_image_file_field, chat_name_field, \
    chat_is_notifying_permitted_field, chat_number_of_unread_field, chat_image_file_thumb_field, chat_last_message_field


class ChatServSerializer(serializers.ModelSerializer):
    """
    Need to transmit context 'request_user_id'
    """

    image_file = chat_image_file_field.ChatImageFileField(read_only=True)
    name = chat_name_field.ChatNameField(read_only=True)
    user_member_list = user_serializers.UserServMiniSerializer(read_only=True, many=True)
    is_notifying_permitted = chat_is_notifying_permitted_field.ChatIsNotifyingPermittedField(read_only=True)
    last_message = chat_last_message_field.ChatLastMessageField(read_only=True)
    number_of_unread = chat_number_of_unread_field.ChatNumberOfUnreadField(read_only=True)
    image_file_thumb = chat_image_file_thumb_field.ChatImageFileThumbField(read_only=True)

    class Meta:
        model = chat.Chat
        fields = ['id', 'image_file', 'name', 'user_member_list', 'is_notifying_permitted', 'last_message',
                  'number_of_unread', 'image_file_thumb', 'is_group_chat']
