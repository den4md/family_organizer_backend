from rest_framework import serializers

from family_organizer import settings


class InviteLinkField(serializers.Field):
    def to_internal_value(self, data):
        pass

    def to_representation(self, value):
        return settings.INVITE_INTENT + 'group/join/' + value