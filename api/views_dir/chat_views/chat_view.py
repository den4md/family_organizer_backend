from typing import Optional

from api.models_dir import group, chat
from api.serializers_dir import chat_serializers
from api.views_dir import base_view


class ChatView(base_view.BaseView):
    url_parameters = ['group_id', 'chat_id']

    def handle_get(self) -> Optional[base_view.BaseView]:
        self.response_dict['chat_data'] = \
            chat_serializers.ChatServSerializer(self.dict['chat'],
                                                context={'request_user_id': self.request.user.id}).data
        return self

    def chain_get(self):
        self.authorize() \
            .require_url_parameters(self.url_parameters) \
            .get_model_by_id(group.Group, self.request.GET['group_id']) \
            .user_belong_to_group() \
            .get_model_by_id(chat.Chat, self.request.GET['chat_id']) \
            .model_belong_to_group('chat') \
            .request_handlers['GET']['specific'](self)

    request_handlers = {
        'GET': {
            'chain': chain_get,
            'specific': handle_get
        }
    }
