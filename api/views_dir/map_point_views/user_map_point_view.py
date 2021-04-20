from typing import Optional

from api.serializers_dir import user_map_point_serializers
from api.views_dir import base_view


class UserMapPointView(base_view.BaseView):

    def handle_post(self) -> Optional[base_view.BaseView]:
        self.request.user.user_map_point_list.all().delete()
        self.dict['serializer'].save(user=self.request.user)
        return self

    def chain_post(self):
        self.authorize() \
            .deserialize_json_body() \
            .body_match_app_serializer(user_map_point_serializers.UserMapPointAppSerializer) \
            .app_serializer_validation(user_map_point_serializers.UserMapPointAppSerializer) \
            .request_handlers['POST']['specific'](self)
    
    request_handlers = {
        'POST': {
            'chain': chain_post,
            'specific': handle_post
        }
    }
