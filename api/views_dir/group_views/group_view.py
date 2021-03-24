import hashlib
from typing import Optional

from django.utils import timezone

from api.helpers import validate_type, image_helper
from api.models_dir import file, chat, group
from api.serializers_dir import group_serializers
from api.views_dir import base_view
from family_organizer import settings


class GroupView(base_view.BaseView):
    url_parameters = ['group_id']

    def handle_post(self: base_view.BaseView) -> Optional[base_view.BaseView]:

        if 'file' in self.dict.keys() and self.dict['file']:
            image_file_thumb = image_helper.make_thumbnail_base64_str(self.dict['file'].file_path)
        else:
            self.dict['file'] = None
            image_file_thumb = None

        new_group = self.dict['serializer'].save(user_creator=self.request.user, image_file=self.dict['file'],
                                                 image_file_thumb=image_file_thumb)
        if self.dict['file']:
            self.dict['file'].group = new_group
            self.dict['file'].save()

        today_hash = hashlib.md5(str(timezone.now()).encode('utf8')).hexdigest()
        new_group.invite_id = today_hash[:16] + str(new_group.id) + today_hash[16:]

        new_group.user_member_list.add(self.request.user)

        lonely_group_chat = chat.Chat(group=new_group, is_main_group_chat=True, is_group_chat=True)
        lonely_group_chat.save()
        lonely_group_chat.user_member_list.add(self.request.user)
        lonely_group_chat.save()

        new_group.save()

        self.response_dict['group_id'] = new_group.id
        self.status_code = 201
        return self

    def process_image_file(self: base_view.BaseView) -> Optional[base_view.BaseView]:
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
        if self.dict['file'].type not in settings.IMAGE_TYPES:
            return self.error(f'Wrong type of image ("{self.dict["file"].type}")'
                              f'. Allowed types: ' +
                              '"' + '", "'.join(settings.IMAGE_TYPES) + '"')
        if self.dict['file'].user_uploader != self.request.user or self.dict['file'].group:
            return self.error(f'This file can\'t be used as group avatar, '
                              f'because is already used by other group/other user')
        if self.dict['file'] == self.request.user.image_file:
            return self.error(f'Can\'t use same image for profile and group avatars at one time')
        return self

    # noinspection PyUnresolvedReferences
    def chain_post(self: base_view.BaseView):
        self.authorize() \
            .deserialize_json_body() \
            .body_match_app_serializer(group_serializers.GroupAppSerializer) \
            .app_serializer_validation(group_serializers.GroupAppSerializer) \
            .process_image_file() \
            .request_handlers['POST']['specific'](self)

    def handle_get(self: base_view.BaseView) -> Optional[base_view.BaseView]:
        self.response_dict['group_data'] = group_serializers.GroupServSerializer(self.dict['group']).data
        return self

    def chain_get(self: base_view.BaseView):
        self.authorize() \
            .require_url_parameters(self.url_parameters) \
            .get_model_by_id(group.Group, self.request.GET['group_id']) \
            .user_belong_to_group() \
            .request_handlers['GET']['specific'](self)

    def handle_put(self: base_view.BaseView) -> Optional[base_view.BaseView]:
        if 'file' in self.dict.keys():
            if self.dict['group'].image_file != self.dict['file']:
                if self.dict['group'].image_file:
                    self.dict['group'].image_file.delete()
                    self.dict['group'].image_file = None
                    self.dict['group'].image_file_thumb = None
                if self.dict['file']:
                    self.dict['group'].image_file = self.dict['file']
                    self.dict['group'].image_file_thumb = image_helper.make_thumbnail_base64_str(self.dict['file'].file_path)
                    self.dict['file'].group = self.dict['group']
                    self.dict['file'].save()

        self.dict['group'].save()
        return self

    # noinspection PyUnresolvedReferences
    def chain_put(self: base_view.BaseView):
        self.authorize() \
            .require_url_parameters(self.url_parameters) \
            .get_model_by_id(group.Group, self.request.GET['group_id']) \
            .user_belong_to_group() \
            .deserialize_json_body() \
            .body_match_app_serializer(group_serializers.GroupAppSerializer, required=False) \
            .put_serializer(self.dict['group'], group_serializers.GroupAppSerializer) \
            .process_image_file() \
            .request_handlers['PUT']['specific'](self)

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
        }
    }
