from rest_framework import serializers


class ChatNameField(serializers.Field):
    def to_internal_value(self, data):
        pass

    def get_attribute(self, instance):
        return instance

    def to_representation(self, value):
        if value.is_main_group_chat:
            return value.group.name
        elif not value.is_group_chat:
            other_user = value.user_member_list.exclude(id=self.context['request_user_id']).get()
            return f'{other_user.first_name} {other_user.last_name}'
        else:
            return 'Chat'
