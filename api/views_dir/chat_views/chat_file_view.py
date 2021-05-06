from typing import Optional

from api.models_dir import group, chat, file
from api.views_dir import base_view


class ChatFileView(base_view.BaseView):
    url_parameters = ['group_id', 'chat_id']

    def handle_post(self) -> Optional[base_view.BaseView]:
        if 'file_id' not in self.dict['body_json']:
            return self.error(f'Can\'t find "file_id" in body')
        if not isinstance(self.dict['body_json']['file_id'], int):
            return self.error(f'Field "file_id" isn\'t a <Int> type')

        if not self.get_model_by_id(file.File, self.dict['body_json']['file_id']) or \
                not self.model_belong_to_group('file'):
            return

        self.dict['chat'].chat_message_list.exclude(user_sender=self.request.user).filter(is_read=False) \
            .update(is_read=True)
        self.dict['chat'].chat_user_settings.filter(user=self.request.user).update(number_of_unread_messages=0)

        for chat_user_setting in self.dict['chat'].chat_user_settings.exclude(user=self.request.user).iterator():
            chat_user_setting.number_of_unread_messages += 1
            chat_user_setting.save()

        self.dict['chat'].chat_message_list.create(is_text=False, text='', file=self.dict['file'],
                                                   user_sender=self.request.user)

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
