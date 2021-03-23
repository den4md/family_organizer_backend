from rest_framework import serializers

from api.models_dir import group
from api.serializers_dir import base_app_serializer, file_serializers, user_serializers
from api.serializers_dir.custom_fields.invite_link_field import InviteLinkField
from api.serializers_dir.custom_fields.string_date_field import StringDateField


class GroupAppSerializer(base_app_serializer.BaseAppSerializer):
    class Meta:
        model = group.Group

        required_fields = {'name'}
        non_required_fields = {'image_file_id'}
        possible_fields = required_fields | non_required_fields
        non_serialized_fields = {'image_file_id'}
        fields = list(possible_fields - non_serialized_fields)


class GroupServSerializer(serializers.ModelSerializer):
    image_file = file_serializers.FileServSerializer(read_only=True)
    user_member_list = user_serializers.UserServMiniSerializer(many=True, read_only=True)
    create_date = StringDateField()
    user_creator = user_serializers.UserServMiniSerializer(read_only=True)
    invite_link = InviteLinkField(source='invite_id')

    class Meta:
        model = group.Group
        fields = ['id', 'name', 'image_file', 'user_member_list', 'create_date', 'user_creator', 'invite_link']


class GroupServMiniSerializer(serializers.ModelSerializer):
    image_file = file_serializers.FileServSerializer(read_only=True)
    invite_link = InviteLinkField(source='invite_id')

    class Meta:
        model = group.Group
        fields = ['id', 'name', 'image_file', 'invite_link']
