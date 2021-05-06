from typing import Optional

from api.models_dir import group
from api.serializers_dir import chat_serializers
from api.views_dir import base_view


class ChatListView(base_view.BaseView):
    url_parameters = ['group_id']

    def handle_get(self) -> Optional[base_view.BaseView]:
        self.response_dict['chat_list'] = \
            chat_serializers.ChatServSerializer(self.dict['group'].chat_list.filter(user_member_list=self.request.user),
                                                many=True, context={'request_user_id': self.request.user.id}).data
        return self

    def chain_get(self):
        self.authorize() \
            .require_url_parameters(self.url_parameters) \
            .get_model_by_id(group.Group, self.request.GET['group_id']) \
            .user_belong_to_group() \
            .request_handlers['GET']['specific'](self)

    request_handlers = {
        'GET': {
            'chain': chain_get,
            'specific': handle_get
        }
    }
