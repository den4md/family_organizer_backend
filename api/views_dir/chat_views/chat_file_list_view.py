from typing import Optional

from api.models_dir import group, chat, file
from api.serializers_dir import file_serializers
from api.views_dir import base_view


class ChatFileListView(base_view.BaseView):
    url_parameters = ['group_id', 'chat_id']

    def handle_get(self) -> Optional[base_view.BaseView]:
        self.response_dict['chat_file_list'] = \
            file_serializers.FileServSerializer(file.File.objects.filter(
                id__in=self.dict['chat'].chat_message_list.filter(is_text=False).values_list('file', flat=True)),
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
