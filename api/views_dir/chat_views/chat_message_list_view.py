from typing import Optional

from api.models_dir import group, chat
from api.serializers_dir import chat_message_serializers
from api.views_dir import base_view


class ChatMessageListView(base_view.BaseView):
    url_parameters = ['group_id', 'chat_id']

    def handle_get(self) -> Optional[base_view.BaseView]:
        self.dict['chat'].chat_message_list.exclude(user_sender=self.request.user).filter(is_read=False) \
            .update(is_read=True)
        self.dict['chat'].chat_user_settings.filter(user=self.request.user).update(number_of_unread_messages=0)
        self.response_dict['chat_message_list'] = \
            chat_message_serializers.ChatMessageServSerializer(self.dict['chat'].chat_message_list.all(),
                                                               many=True).data
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
