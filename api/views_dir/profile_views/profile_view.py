from __future__ import annotations
from typing import Optional

from django.db import IntegrityError

from api.helpers import validate_type, image_helper
from api.models_dir import file
from api.serializers_dir import user_serializers
from api.views_dir import base_view
from family_organizer import settings


class ProfileView(base_view.BaseView):

    def handle_put(self) -> Optional[ProfileView]:
        try:
            if 'email' in self.dict['body_json'].keys():
                self.request.user.username = self.dict['body_json']['email']
            for field in user_serializers.UserAppSerializer.Meta.non_serialized_fields:
                if field in self.dict['body_json'].keys():
                    if field == 'password_hash':
                        return self.error(f'Can\'t edit password. Use \'/password_change\' instead')

                    # Image ('image_file_id')
                    else:
                        self.put_image_file()
            self.request.user.save()
        except IntegrityError:
            return self.error(f'This email is already in use')
        return self

    def chain_put(self):
        self.authorize() \
            .deserialize_json_body() \
            .body_match_serializer(user_serializers.UserAppSerializer, required=False) \
            .put_serializer(self.request.user, user_serializers.UserAppSerializer) \
            .request_handlers['PUT']['specific'](self)

    def handle_get(self) -> Optional[ProfileView]:
        serializer = user_serializers.UserServSerializer(self.request.user)
        self.response_dict['user_data'] = serializer.data
        self.response_dict['user_data']['date_joined'] = self.request.user.date_joined.strftime('%Y-%m-%d %H:%M')
        return self

    # noinspection PyArgumentList
    def chain_get(self):
        self.authorize() \
            .request_handlers['GET']['specific'](self)

    request_handlers = {
        'GET': {
            'chain': chain_get,
            'specific': handle_get
        },
        'PUT': {
            'chain': chain_put,
            'specific': handle_put
        }
    }

    def put_image_file(self):
        if not validate_type.validate_type(self.dict['body_json']['image_file_id'], int):
            return self.error(f'Wrong type of "image_file_id". Expected - "int", '
                              f'got - "{type(self.dict["body_json"]["image_file_id"])}"')
        if self.dict['body_json']['image_file_id']:
            self.get_model_by_id(file.File, self.dict['body_json']['image_file_id'])
        else:
            self.dict['file'] = None

        if self.request.user.image_file == self.dict['file']:
            return

        # noinspection SpellCheckingInspection
        if self.dict['body_json']['image_file_id']:
            # if not self.dict['file']:
            #     raise Exception(f'File with id "{self.dict["body_json"]["image_file_id"]}" not found'
            #                     f'and DB haven\'t raised "ObjectDoesNotExist"')
            if self.dict['file'].user_uploader != self.request.user or self.dict['file'].group:
                return self.error('This file can\'t be used as avatar, '
                                  'because is already used by group/other user')
            if self.dict['file'].type not in settings.IMAGE_TYPES:
                return self.error(f'Wrong type of image ("{self.dict["file"].type}")'
                                  f'. Allowed types: ' +
                                  '"' + '", "'.join(settings.IMAGE_TYPES) + '"')
            thumb = image_helper.make_thumbnail_base64_str(self.dict['file'].file_path)

        if self.request.user.image_file:
            self.request.user.image_file.delete()
            self.request.user.image_file = None
            self.request.user.image_file_thumb = None
        if self.dict['body_json']['image_file_id']:
            self.request.user.image_file = self.dict['file']
            # noinspection PyUnboundLocalVariable
            self.request.user.image_file_thumb = thumb
