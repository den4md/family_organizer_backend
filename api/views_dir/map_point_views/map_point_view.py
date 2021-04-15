from typing import Optional

from api.helpers import validate_type, image_helper
from api.models_dir import group, file, map_point
from api.serializers_dir import map_point_serializers
from api.views_dir import base_view
from family_organizer import settings


class MapPointView(base_view.BaseView):
    url_parameters = ['group_id', 'map_point_id']

    def process_image_file(self) -> Optional[base_view.BaseView]:
        if 'image_file_id' not in self.dict['body_json'].keys():
            return self
        if not validate_type.validate_type(self.dict['body_json']['image_file_id'], int):
            return self.error(f'Wrong type of "image_file_id". Expected - "int", '
                              f'got - "{type(self.dict["body_json"]["image_file_id"])}"')
        if self.dict['body_json']['image_file_id']:
            if not self.get_model_by_id(file.File, self.dict['body_json']['image_file_id']):
                return
        else:
            self.dict['file'] = None
            return self
        if self.dict['file'].extension not in settings.IMAGE_TYPES:
            return self.error(f'Wrong type of image ("{self.dict["file"].extension}")'
                              f'. Allowed types: ' +
                              '"' + '", "'.join(settings.IMAGE_TYPES) + '"')
        if not (self.dict['file'].group and self.dict['file'].group == self.dict['group']):
            return self.error(f'This file can\'t be used because it\'s already used by other group/other user')
        return self

    def handle_post(self) -> Optional[base_view.BaseView]:
        if 'file' in self.dict.keys() and self.dict['file']:
            image_file_thumb = image_helper.make_thumbnail_base64_str(self.dict['file'].file_path)
        else:
            self.dict['file'] = None
            image_file_thumb = None

        _map_point = self.dict['serializer'].save(user_creator=self.request.user, group=self.dict['group'],
                                                  image_file=self.dict['file'], image_file_thumb=image_file_thumb)
        self.response_dict['map_point_id'] = _map_point.id
        return self

    # noinspection PyUnresolvedReferences
    def chain_post(self):
        self.authorize() \
            .require_url_parameters([self.url_parameters[0]]) \
            .get_model_by_id(group.Group, self.request.GET['group_id']) \
            .user_belong_to_group() \
            .deserialize_json_body() \
            .body_match_app_serializer(map_point_serializers.MapPointAppSerializer) \
            .app_serializer_validation(map_point_serializers.MapPointAppSerializer) \
            .process_image_file() \
            .request_handlers['POST']['specific'](self)

    def handle_get(self) -> Optional[base_view.BaseView]:
        self.response_dict['map_point_data'] = map_point_serializers.MapPointServSerializer(self.dict['map_point']).data
        return self

    def chain_get(self):
        self.authorize() \
            .require_url_parameters(self.url_parameters) \
            .get_model_by_id(group.Group, self.request.GET['group_id']) \
            .user_belong_to_group() \
            .get_model_by_id(map_point.MapPoint, self.request.GET['map_point_id']) \
            .model_belong_to_group('map_point') \
            .request_handlers['GET']['specific'](self)

    def handle_put(self) -> Optional[base_view.BaseView]:
        if 'file' in self.dict.keys() and self.dict['file']:
            image_file_thumb = image_helper.make_thumbnail_base64_str(self.dict['file'].file_path)
        else:
            self.dict['file'] = None
            image_file_thumb = None

        if 'image_file_id' in self.dict['body_json'].keys():
            self.dict['map_point'].image_file = self.dict['file']
            self.dict['map_point'].image_file_thumb = image_file_thumb
        self.dict['map_point'].save()

        return self

    # noinspection PyUnresolvedReferences
    def chain_put(self):
        self.authorize() \
            .require_url_parameters(self.url_parameters) \
            .get_model_by_id(group.Group, self.request.GET['group_id']) \
            .user_belong_to_group() \
            .deserialize_json_body() \
            .body_match_app_serializer(map_point_serializers.MapPointAppSerializer, required=False) \
            .get_model_by_id(map_point.MapPoint, self.request.GET['map_point_id']) \
            .model_belong_to_group('map_point') \
            .put_serializer(self.dict['map_point'], map_point_serializers.MapPointAppSerializer) \
            .process_image_file() \
            .request_handlers['PUT']['specific'](self)

    def handle_delete(self):
        self.dict['map_point'].delete()
        return self

    def chain_delete(self):
        self.authorize() \
            .require_url_parameters(self.url_parameters) \
            .get_model_by_id(group.Group, self.request.GET['group_id']) \
            .user_belong_to_group() \
            .get_model_by_id(map_point.MapPoint, self.request.GET['map_point_id']) \
            .model_belong_to_group('map_point') \
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
