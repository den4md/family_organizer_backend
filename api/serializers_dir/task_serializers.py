from rest_framework import serializers

from api.models_dir import task
from api.serializers_dir import base_app_serializer, file_serializers, user_serializers, subtask_serializers
from api.serializers_dir.custom_fields import string_datetime_field


class TaskAppSerializer(base_app_serializer.BaseAppSerializer):
    class Meta:
        model = task.Task
        required_fields = {'name'}
        non_required_fields = {'description', 'file_id_list', 'deadline_datetime', 'user_responsible_id_list',
                               'subtask_list', 'status'}
        possible_fields = required_fields | non_required_fields
        non_serialized_fields = {'file_id_list', 'user_responsible_id_list', 'subtask_list'}
        fields = list(possible_fields - non_serialized_fields)


class TaskServSerializer(serializers.ModelSerializer):
    file_list = file_serializers.FileServSerializer(many=True, read_only=True)
    deadline_datetime = string_datetime_field.StringDatetimeField(read_only=True)
    user_responsible_list = user_serializers.UserServMiniSerializer(many=True, read_only=True)
    subtask_list = subtask_serializers.SubtaskServSerializer(many=True, read_only=True)
    user_creator = user_serializers.UserServMiniSerializer(read_only=True)

    class Meta:
        model = task.Task
        fields = ['id', 'name', 'description', 'file_list', 'deadline_datetime', 'user_responsible_list',
                  'subtask_list', 'status', 'create_date', 'user_creator', 'is_task']


class TaskServMiniSerializer(serializers.ModelSerializer):
    subtask_list = subtask_serializers.SubtaskServMiniSerializer(many=True, read_only=True)
    deadline_datetime = string_datetime_field.StringDatetimeField(read_only=True)

    class Meta:
        model = task.Task
        fields = ['id', 'name', 'description', 'subtask_list', 'deadline_datetime', 'status', 'is_task']