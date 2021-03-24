from typing import Optional

from django.db import IntegrityError

from api.serializers_dir import user_serializers
from api.views_dir import base_view


class SignUpView(base_view.BaseView):

    def create_new_user(self: base_view.BaseView) -> Optional[base_view.BaseView]:
        try:
            instance = self.dict['serializer'].save(username=self.dict['body_json']['email'])
            instance.set_password(self.dict['body_json']['password_hash'])
            instance.save()
        except IntegrityError:
            return self.error(f'This email is already in use')
        else:
            self.status_code = 201
            return self

    # noinspection PyUnresolvedReferences
    def handle_post(self: base_view.BaseView) -> Optional[base_view.BaseView]:
        return self.no_image_file_id() \
            .create_new_user()

    def chain_post(self: base_view.BaseView):
        self.no_authorize() \
            .deserialize_json_body() \
            .body_match_app_serializer(user_serializers.UserAppSerializer) \
            .app_serializer_validation(user_serializers.UserAppSerializer) \
            .request_handlers['POST']['specific'](self)

    request_handlers = {
        'POST': {
            'chain': chain_post,
            'specific': handle_post
        }
    }
