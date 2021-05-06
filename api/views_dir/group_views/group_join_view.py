from typing import Optional

from django.core import exceptions

from api.models_dir import group, chat
from api.views_dir import base_view


class GroupJoinView(base_view.BaseView):
    url_parameters = ['invite_id']

    def handle_post(self: base_view.BaseView) -> Optional[base_view.BaseView]:
        try:
            self.dict['group'] = group.Group.objects.get(invite_id=self.request.GET['invite_id'])
        except exceptions.ObjectDoesNotExist:
            return self.error(f'Wrong invite or group already does not exist')
        except ValueError as e:
            return self.error(f'Wrong parameter type: \n{str(e)}')
        if not self.user_belong_to_group(need_to_be=False):
            return

        self.dict['group'].user_member_list.add(self.request.user)

        main_group_chat = self.dict['group'].chat_list.get(is_main_group_chat=True)
        main_group_chat.user_member_list.add(self.request.user)
        if main_group_chat.chat_message_list.count():
            main_group_chat.chat_user_settings.get(
                user=self.request.user).number_of_unread_messages = main_group_chat.chat_message_list.count()
            main_group_chat.chat_user_settings.save()

        for non_main_group_chat in self.dict['group'].chat_list \
                .filter(is_main_group_chat=False, is_group_chat=True, chat_message_list__user_sender=self.request.user):
            non_main_group_chat.user_member_list.add(self.request.user)
            if non_main_group_chat.chat_message_list.count():
                non_main_group_chat.chat_user_settings.get(
                    user=self.request.user).number_of_unread_messages = non_main_group_chat.chat_message_list.count()
                non_main_group_chat.chat_user_settings.save()

        other_users = self.dict['group'].user_member_list.exclude(id=self.request.user.id)
        for user_chat in chat.Chat.objects.filter(is_group_chat=False, group=self.dict['group'],
                                                  chat_user_settings__user=self.request.user):
            other_users = other_users.difference(user_chat.user_member_list.all())
        for other_user in other_users.iterator():
            self.dict['group'].chat_list.create().user_member_list.add(other_user, self.request.user)

        self.response_dict['group_id'] = self.dict['group'].id
        return self

    def chain_post(self: base_view.BaseView):
        self.authorize() \
            .require_url_parameters(self.url_parameters) \
            .request_handlers['POST']['specific'](self)

    request_handlers = {
        'POST': {
            'chain': chain_post,
            'specific': handle_post
        }
    }
