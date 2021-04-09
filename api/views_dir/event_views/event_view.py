from typing import Optional

from api.models_dir import file, map_point, event, group
from api.serializers_dir import event_serializers
from api.views_dir import base_view


class EventView(base_view.BaseView):
    url_parameters = ['group_id', 'event_id']

    def attach_files(self, file_id_list: list, file_list: list) -> Optional[base_view.BaseView]:
        for file_id in file_id_list:
            if not self.get_model_by_id(file.File, file_id) or self.dict['file'].group != self.dict['group']:
                self.error('Can\'t attach this file (doesn\'t exist or doesn\'t belong to group)')
                return None
            file_list.append(self.dict['file'])
        return self

    def handle_post(self) -> Optional[base_view.BaseView]:
        self.dict['file_list'] = []
        if 'file_id_list' in self.dict['body_json'].keys():
            if not self.attach_files(self.dict['body_json']['file_id_list'], self.dict['file_list']):
                return None
        if 'map_point_id' in self.dict['body_json'].keys():
            if not self.get_model_by_id(map_point.MapPoint, self.dict['body_json']['map_point_id']) or \
                    self.dict['map_point'].group != self.dict['group']:
                self.error('Can\'t attach this map point (doesn\'t exist or doesn\'t belong to group)')
                return None

        event_ = self.dict['serializer'].save(user_creator=self.request.user, group=self.dict['group'])

        for file_ in self.dict['file_list']:
            event_.file_list.add(file_)
        if 'map_point_id' in self.dict['body_json'].keys():
            event_.map_point = self.dict['map_point']
        self.response_dict['event_id'] = event_.id
        return self

    def chain_post(self):
        self.authorize() \
            .require_url_parameters([self.url_parameters[0]]) \
            .get_model_by_id(group.Group, self.request.GET['group_id']) \
            .user_belong_to_group() \
            .deserialize_json_body() \
            .body_match_app_serializer(event_serializers.EventAppSerializer) \
            .app_serializer_validation(event_serializers.EventAppSerializer) \
            .request_handlers['POST']['specific'](self)

    def handle_get(self) -> Optional[base_view.BaseView]:
        self.response_dict['event_data'] = event_serializers.EventServSerializer(self.dict['event']).data
        return self

    def chain_get(self):
        self.authorize() \
            .require_url_parameters(self.url_parameters) \
            .get_model_by_id(group.Group, self.request.GET['group_id']) \
            .user_belong_to_group() \
            .get_model_by_id(event.Event, self.request.GET['event_id']) \
            .model_belong_to_group('event') \
            .request_handlers['GET']['specific'](self)

    def handle_put(self) -> Optional[base_view.BaseView]:
        self.dict['file_list'] = []
        if 'file_id_list' in self.dict['body_json'].keys():
            if not self.attach_files(self.dict['body_json']['file_id_list'], self.dict['file_list']):
                return None
        if 'map_point_id' in self.dict['body_json'].keys():
            if not self.get_model_by_id(map_point.MapPoint, self.dict['body_json']['map_point_id']) or \
                    self.dict['map_point'].group != self.dict['group']:
                self.error('Can\'t attach this map point (doesn\'t exist or doesn\'t belong to group)')
                return None

        self.dict['event'].save()

        if 'file_id_list' in self.dict['body_json'].keys():
            self.dict['event'].file_list.clear()
            for file_ in self.dict['file_list']:
                self.dict['event'].file_list.add(file_)
        if 'map_point_id' in self.dict['body_json'].keys():
            self.dict['event'].map_point = self.dict['map_point']
        return self

    def chain_put(self):
        self.authorize() \
            .require_url_parameters(self.url_parameters) \
            .get_model_by_id(group.Group, self.request.GET['group_id']) \
            .user_belong_to_group() \
            .deserialize_json_body() \
            .body_match_app_serializer(event_serializers.EventAppSerializer, required=False) \
            .get_model_by_id(event.Event, self.request.GET['event_id']) \
            .model_belong_to_group('event') \
            .put_serializer(self.dict['event'], event_serializers.EventAppSerializer) \
            .request_handlers['PUT']['specific'](self)

    def handle_delete(self) -> Optional[base_view.BaseView]:
        self.dict['event'].delete()
        return self

    def chain_delete(self):
        self.authorize() \
            .require_url_parameters(self.url_parameters) \
            .get_model_by_id(group.Group, self.request.GET['group_id']) \
            .user_belong_to_group() \
            .get_model_by_id(event.Event, self.request.GET['event_id']) \
            .model_belong_to_group('event') \
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
