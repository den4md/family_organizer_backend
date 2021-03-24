from typing import Optional
from django.db.models import Count

from api.models_dir import group
from api.views_dir import base_view


class GroupLeaveView(base_view.BaseView):
    url_parameters = ['group_id']

    def handle_post(self: base_view.BaseView) -> Optional[base_view.BaseView]:
        # If it is last user in group, then empty group will be deleted entirely
        if self.dict['group'].user_member_list.all().count() == 1:
            self.dict['group'].delete()
            return self

        # Delete private empty non-group chats
        self.dict['group'].chat_list.annotate(Count('chat_message_list')).filter(
            is_group_chat=False, chat_message_list__count=0, chat_user_settings__user=self.request.user).delete()

        # Remove from group chats
        for group_chat in self.dict['group'].chat_list.filter(is_group_chat=True, user_member_list=self.request.user) \
                .iterator():
            group_chat.user_member_list.remove(self.request.user)

        # Delete empty group chats
        self.dict['group'].chat_list.annotate(Count('chat_message_list')).annotate(Count('user_member_list')).filter(
            is_group_chat=True, chat_message_list__count=0, user_member_list__count=0).delete()

        self.dict['group'].user_member_list.remove(self.request.user)
        return self

    def chain_post(self):
        self.authorize() \
            .require_url_parameters(self.url_parameters) \
            .get_model_by_id(group.Group, self.request.GET['group_id']) \
            .user_belong_to_group() \
            .request_handlers['POST']['specific'](self)

    request_handlers = {
        'POST': {
            'chain': chain_post,
            'specific': handle_post
        }
    }
