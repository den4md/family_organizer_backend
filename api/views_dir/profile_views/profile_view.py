import os
from typing import Optional

from django.db import IntegrityError

from api.helpers import validate_type, image_helper
from api.models_dir import file
from api.serializers_dir import user_serializers
from api.views_dir import base_view
from api.views_dir.group_views import group_leave_view
from family_organizer import settings


class ProfileView(base_view.BaseView):
    url_parameters = ['password_hash']

    def handle_put(self: base_view.BaseView) -> Optional[base_view.BaseView]:
        try:
            if 'email' in self.dict['body_json'].keys():
                self.request.user.username = self.dict['body_json']['email']
            self.request.user.save()
        except IntegrityError:
            return self.error(f'This email is already in use')
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

        if self.request.user.image_file == self.dict['file']:
            return self

        # noinspection SpellCheckingInspection
        if self.dict['body_json']['image_file_id']:
            # if not self.dict['file']:
            #     raise Exception(f'File with id "{self.dict["body_json"]["image_file_id"]}" not found'
            #                     f'and DB haven\'t raised "ObjectDoesNotExist"')
            if self.dict['file'].user_uploader != self.request.user or self.dict['file'].group:
                return self.error('This file can\'t be used as profile avatar, '
                                  'because is already used by group/other user')
            if self.dict['file'].extension not in settings.IMAGE_TYPES:
                return self.error(f'Wrong type of image ("{self.dict["file"].extension}")'
                                  f'. Allowed types: ' +
                                  '"' + '", "'.join(settings.IMAGE_TYPES) + '"')
            image_file_thumb = image_helper.make_thumbnail_base64_str(self.dict['file'].file_path)

        if self.request.user.image_file:
            os.remove(settings.FILE_STORAGE + self.request.user.image_file.file_path)
            self.request.user.image_file.delete()
            self.request.user.image_file = None
            self.request.user.image_file_thumb = None
        if self.dict['body_json']['image_file_id']:
            self.request.user.image_file = self.dict['file']
            # noinspection PyUnboundLocalVariable
            self.request.user.image_file_thumb = image_file_thumb
        return self

    def no_password_hash(self: base_view.BaseView) -> Optional[base_view.BaseView]:
        if 'password_hash' not in self.dict['body_json'].keys():
            return self
        else:
            return self.error(f'Can\'t edit password. Use \'/password_change\' instead')

    # noinspection PyUnresolvedReferences
    def chain_put(self: base_view.BaseView):
        self.authorize() \
            .deserialize_json_body() \
            .body_match_app_serializer(user_serializers.UserAppSerializer, required=False) \
            .put_serializer(self.request.user, user_serializers.UserAppSerializer) \
            .no_password_hash() \
            .process_image_file() \
            .request_handlers['PUT']['specific'](self)

    def handle_get(self: base_view.BaseView) -> Optional[base_view.BaseView]:
        serializer = user_serializers.UserServSerializer(self.request.user)
        self.response_dict['user_data'] = serializer.data
        return self

    # noinspection PyArgumentList
    def chain_get(self: base_view.BaseView):
        self.authorize() \
            .request_handlers['GET']['specific'](self)

    def handle_delete(self: base_view.BaseView) -> Optional[base_view.BaseView]:
        if self.request.user.check_password(self.request.GET['password_hash']):
            for group in self.request.user.group_list:
                self.dict['group'] = group
                group_leave_view.GroupLeaveView.request_handlers['POST']['specific'](self)
            for user_file in self.request.file_list:
                if user_file.group:
                    os.remove(settings.FILE_STORAGE + user_file.path)
                    user_file.delete()
            self.request.user.delete()
            return self
        else:
            return self.error(f'Wrong current password')

    def chain_delete(self: base_view.BaseView):
        self.authorize() \
            .require_url_parameters(self.url_parameters) \
            .request_handlers['DELETE']['specific'](self)

    request_handlers = {
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
