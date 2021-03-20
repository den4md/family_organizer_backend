from __future__ import annotations
from typing import Optional

from django.db import IntegrityError

from api.serializers_dir import user_app_serializer
from api.views_dir import base_view


class SignUpView(base_view.BaseView):
    def no_image_file_id(self) -> Optional[SignUpView]:
        if 'image_file_id' not in self.dict['body_json'].keys():
            return self
        else:
            self.response_dict['result'] = f'Image for registration is forbidden'
            self.status_code = 400

    def create_new_user(self) -> Optional[SignUpView]:
        try:
            instance = self.dict['serializer'].save(username=self.dict['body_json']['email'])
            instance.set_password(self.dict['body_json']['password_hash'])
            instance.save()
        except IntegrityError:
            self.response_dict['result'] = f'This email is already in use'
            self.status_code = 400
        else:
            self.status_code = 201
            return self

    def handle_post(self):
        self.no_image_file_id()\
            .create_new_user()

    def view_post(self):
        self.no_authorize()\
            .deserialize_json_body()\
            .body_match_serializer(user_app_serializer.UserAppSerializer)\
            .deserializer_validation(user_app_serializer.UserAppSerializer)\
            .specific_handlers['POST'](self)

    specific_handlers = {
        'POST': handle_post
    }

    method_handlers = {
        'POST': view_post
    }
