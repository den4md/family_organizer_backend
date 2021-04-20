from typing import Optional

from rest_framework.exceptions import ValidationError

from api.models_dir import file, user, group, task
from api.serializers_dir import task_serializers, subtask_serializers
from api.views_dir import base_view


class TaskView(base_view.BaseView):
    url_parameters = ['group_id', 'note_id']

    def attach_files(self, file_id_list: list, file_list: list) -> Optional[base_view.BaseView]:
        self.dict['is_task'] = True
        if file_id_list is None:
            return self
        if not isinstance(file_id_list, list):
            return self.error(f'"file_id_list" isn\'t a list')
        for file_id in file_id_list:
            if not self.get_model_by_id(file.File, file_id) or not self.model_belong_to_group('file'):
                return
            file_list.append(self.dict['file'])
        return self

    def attach_responsible(self, user_responsible_id_list: list,
                           user_responsible_list: list) -> Optional[base_view.BaseView]:
        self.dict['is_task'] = True
        if user_responsible_id_list is None:
            return self
        if not isinstance(user_responsible_id_list, list):
            return self.error(f'"user_responsible_id_list" isn\'t a list')
        for user_id in user_responsible_id_list:
            if not self.get_model_by_id(user.User, user_id) or not self.model_belong_to_group('user'):
                return
            user_responsible_list.append(self.dict['user'])
        return self

    def serialize_subtask(self, subtask_json: dict, subtask: dict) -> Optional[base_view.BaseView]:
        if not isinstance(subtask_json, dict):
            return self.error(f'"subtask" isn\'t a object')
        for key in subtask_json.keys():
            if key not in subtask_serializers.SubtaskAppSerializer.Meta.possible_fields:
                return self.error(f'Can\'t edit value for "{str(key)}"')
        for required_field in subtask_serializers.SubtaskAppSerializer.Meta.required_fields:
            if required_field not in subtask_json.keys():
                return self.error(f'Can\'t find value for "{str(required_field)}", but it\'s required')
        subtask['serializer'] = subtask_serializers.SubtaskAppSerializer(data=subtask_json)
        try:
            subtask['serializer'].is_valid(raise_exception=True)
        except ValidationError as e:
            return self.error(f'Error while validating object: {str(e)}')
        subtask['file_list'] = []
        if 'file_id_list' in subtask_json.keys():
            if not self.attach_files(subtask_json['file_id_list'], subtask['file_list']):
                return
        subtask['user_responsible_list'] = []
        if 'user_responsible_id_list' in subtask_json.keys():
            if not self.attach_responsible(subtask_json['user_responsible_id_list'],
                                           subtask['user_responsible_list']):
                return
        return self

    def attach_subtasks(self) -> Optional[base_view.BaseView]:
        self.dict['is_task'] = True
        if self.dict['body_json']['subtask_list'] is None:
            return self
        if not isinstance(self.dict['body_json']['subtask_list'], list):
            return self.error(f'"subtask_list" isn\'t a list')
        for task_ in self.dict['body_json']['subtask_list']:
            self.dict['subtask_list'].append(dict())
            if not self.serialize_subtask(task_, self.dict['subtask_list'][-1]):
                return
        return self

    def handle_post(self) -> Optional[base_view.BaseView]:
        if ('status' in self.dict['body_json'].keys() and (self.dict['body_json']['status'] is not None and
                                                           self.dict['body_json']['status'] != 'not available')) or (
                'deadline_datetime' in self.dict['body_json'].keys() and
                self.dict['body_json']['deadline_datetime'] is not None):
            self.dict['is_task'] = True
        else:
            self.dict['is_task'] = False

        self.dict['file_list'] = []
        if 'file_id_list' in self.dict['body_json'].keys():
            if not self.attach_files(self.dict['body_json']['file_id_list'], self.dict['file_list']):
                return
        self.dict['user_responsible_list'] = []
        if 'user_responsible_id_list' in self.dict['body_json'].keys():
            if not self.attach_responsible(self.dict['body_json']['user_responsible_id_list'],
                                           self.dict['user_responsible_list']):
                return
        self.dict['subtask_list'] = []
        if 'subtask_list' in self.dict['body_json'].keys():
            if not self.attach_subtasks():
                return

        # All validation was passed
        # Building

        task_ = self.dict['serializer'].save(user_creator=self.request.user, is_task=self.dict['is_task'],
                                             group=self.dict['group'])
        for file_ in self.dict['file_list']:
            task_.file_list.add(file_)
        for user_ in self.dict['user_responsible_list']:
            task_.user_responsible_list.add(user_)

        for subtask_dict in self.dict['subtask_list']:
            subtask = subtask_dict['serializer'].save(user_creator=self.request.user, task=task_)
            for file_ in subtask_dict['file_list']:
                subtask.file_list.add(file_)
            for user_ in subtask_dict['user_responsible_list']:
                subtask.user_responsible_list.add(user_)
            task_.subtask_list.add(subtask)
        self.response_dict['note_id'] = task_.id
        return self

    def chain_post(self):
        self.authorize() \
            .require_url_parameters([self.url_parameters[0]]) \
            .get_model_by_id(group.Group, self.request.GET['group_id']) \
            .user_belong_to_group() \
            .deserialize_json_body() \
            .body_match_app_serializer(task_serializers.TaskAppSerializer) \
            .app_serializer_validation(task_serializers.TaskAppSerializer) \
            .request_handlers['POST']['specific'](self)

    def handle_get(self) -> Optional[base_view.BaseView]:
        self.response_dict['note_data'] = task_serializers.TaskServSerializer(self.dict['task']).data
        return self

    def chain_get(self):
        self.authorize() \
            .require_url_parameters(self.url_parameters) \
            .get_model_by_id(group.Group, self.request.GET['group_id']) \
            .user_belong_to_group() \
            .get_model_by_id(task.Task, self.request.GET['note_id']) \
            .model_belong_to_group('task') \
            .request_handlers['GET']['specific'](self)

    def handle_put(self) -> Optional[base_view.BaseView]:
        if (self.dict['task'].status is not None and self.dict['task'].status != 'not available') or \
                self.dict['task'].deadline_datetime is not None:
            self.dict['is_task'] = True
        else:
            self.dict['is_task'] = False

        if 'file_id_list' in self.dict['body_json'].keys():
            self.dict['file_list'] = []
            if not self.attach_files(self.dict['body_json']['file_id_list'], self.dict['file_list']):
                return
        if 'user_responsible_id_list' in self.dict['body_json'].keys():
            self.dict['user_responsible_list'] = []
            if not self.attach_responsible(self.dict['body_json']['user_responsible_id_list'],
                                           self.dict['user_responsible_list']):
                return
        if 'subtask_list' in self.dict['body_json'].keys():
            self.dict['subtask_list'] = []
            if not self.attach_subtasks():
                return

        self.dict['task'].is_task = self.dict['is_task']
        self.dict['task'].save()

        if 'file_id_list' in self.dict['body_json'].keys():
            self.dict['task'].file_list.clear()
            for file_ in self.dict['file_list']:
                self.dict['task'].file_list.add(file_)
        if 'user_responsible_id_list' in self.dict['body_json'].keys():
            self.dict['task'].user_responsible_list.clear()
            for user_ in self.dict['user_responsible_list']:
                self.dict['task'].user_responsible_list.add(user_)

        if 'subtask_list' in self.dict['body_json'].keys():
            self.dict['task'].subtask_list.all().delete()
            for subtask_dict in self.dict['subtask_list']:
                subtask = subtask_dict['serializer'].save(user_creator=self.request.user, task=self.dict['task'])
                for file_ in subtask_dict['file_list']:
                    subtask.file_list.add(file_)
                for user_ in subtask_dict['user_responsible_list']:
                    subtask.user_responsible_list.add(user_)
                self.dict['task'].subtask_list.add(subtask)
        return self

    def chain_put(self):
        self.authorize() \
            .require_url_parameters(self.url_parameters) \
            .get_model_by_id(group.Group, self.request.GET['group_id']) \
            .user_belong_to_group() \
            .deserialize_json_body() \
            .body_match_app_serializer(task_serializers.TaskAppSerializer, required=False) \
            .get_model_by_id(task.Task, self.request.GET['note_id']) \
            .model_belong_to_group('task') \
            .put_serializer(self.dict['task'], task_serializers.TaskAppSerializer) \
            .request_handlers['PUT']['specific'](self)

    def handle_delete(self) -> Optional[base_view.BaseView]:
        self.dict['task'].delete()
        return self

    def chain_delete(self):
        self.authorize() \
            .require_url_parameters(self.url_parameters) \
            .get_model_by_id(group.Group, self.request.GET['group_id']) \
            .user_belong_to_group() \
            .get_model_by_id(task.Task, self.request.GET['note_id']) \
            .model_belong_to_group('task') \
            .request_handlers['DELETE']['specific'](self)

    request_handlers = {
        'POST': {
            'chain': chain_post,
            'specific': handle_post
        },
        'GET': {
            'chain': chain_get,
            'specific': handle_get
        },
        'PUT': {
            'chain': chain_put,
            'specific': handle_put
        },
        'DELETE': {
            'chain': chain_delete,
            'specific': handle_delete
        }
    }
