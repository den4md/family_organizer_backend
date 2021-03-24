from typing import Optional

from api.serializers_dir import group_serializers
from api.views_dir import base_view


class GroupListView(base_view.BaseView):

    def handle_get(self: base_view.BaseView) -> Optional[base_view.BaseView]:
        self.response_dict['group_list'] = group_serializers.GroupServMiniSerializer(self.request.user.group_list.all(),
                                                                                     many=True).data
        return self

    # noinspection PyArgumentList
    def chain_get(self: base_view.BaseView):
        self.authorize() \
            .request_handlers['GET']['specific'](self)

    request_handlers = {
        'GET': {
            'chain': chain_get,
            'specific': handle_get
        }
    }
