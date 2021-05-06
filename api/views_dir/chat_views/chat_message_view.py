from typing import Optional

from api.models_dir import group, chat
from api.views_dir import base_view


class ChatMessageView(base_view.BaseView):
    url_parameters = ['group_id', 'chat_id']

    def handle_post(self) -> Optional[base_view.BaseView]:
        if 'chat_message_data' not in self.dict['body_json']:
            return self.error(f'Can\'t find "chat_message_data" in body')
        if not isinstance(self.dict['body_json']['chat_message_data'], str):
            return self.error(f'Field "chat_message_data" isn\'t a <String> type')

        self.dict['chat'].chat_message_list.exclude(user_sender=self.request.user).filter(is_read=False) \
            .update(is_read=True)
        self.dict['chat'].chat_user_settings.filter(user=self.request.user).update(number_of_unread_messages=0)

        for chat_user_setting in self.dict['chat'].chat_user_settings.exclude(user=self.request.user).iterator():
            chat_user_setting.number_of_unread_messages += 1
            chat_user_setting.save()

        self.dict['chat'].chat_message_list.create(is_text=True, text=self.dict['body_json']['chat_message_data'],
                                                   file=None, user_sender=self.request.user)

        return self

    def chain_post(self):
        self.authorize() \
            .require_url_parameters(self.url_parameters) \
            .get_model_by_id(group.Group, self.request.GET['group_id']) \
            .user_belong_to_group() \
            .get_model_by_id(chat.Chat, self.request.GET['chat_id']) \
            .model_belong_to_group('chat') \
            .deserialize_json_body() \
            .request_handlers['POST']['specific'](self)

    request_handlers = {
            'POST': {
                'chain': chain_post,
                'specific': handle_post
            }
        }
