from __future__ import annotations
from typing import Optional

from django.db import IntegrityError

from api.models_dir import file
from api.serializers_dir import user_serializers
from api.views_dir import base_view


class ProfileView(base_view.BaseView):

    def handle_put(self) -> Optional[ProfileView]:
        try:
            if 'email' in self.dict['body_json'].keys():
                self.request.user.username = self.dict['body_json']['email']
            for field in user_serializers.UserAppSerializer.Meta.non_serialized_fields:
                if field in self.dict['body_json'].keys():
                    if field == 'password_hash':
                        self.response_dict['result'] = f'Can\'t edit password. Use \'/password_change\' instead'
                        self.status_code = 400
                        return

                    # TODO finish image adding
                    # - delete previous image
                    # - creating thumbnail (minimize + Base64)

                    # Image ('image_file_id')
                    # else:
                    #     if self.validate(self.dict['body_json']['image_file_id'], int):
                    #         self.get_model_by_id(file.File, self.dict['body_json']['image_file_id'])
                    #     else:
                    #         pass

            self.request.user.save()
        except IntegrityError:
            self.response_dict['result'] = f'This email is already in use'
            self.status_code = 400
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
