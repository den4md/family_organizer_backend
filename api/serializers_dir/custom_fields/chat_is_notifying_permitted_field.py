from rest_framework import serializers


class ChatIsNotifyingPermittedField(serializers.Field):
    def to_internal_value(self, data):
        pass

    def get_attribute(self, instance):
        return instance

    def to_representation(self, value):
        return value.chat_user_settings.get(user__id=self.context['request_user_id']).is_notifying
