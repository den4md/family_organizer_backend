import datetime
from typing import Optional

from api.models_dir import group
from api.serializers_dir import event_serializers
from api.views_dir import base_view


class EventListView(base_view.BaseView):
    url_parameters = ['group_id']

    def handle_get(self) -> Optional[base_view.BaseView]:
        event_list = self.dict['group'].event_list.all()
        if 'start_date' in self.request.GET.keys() and self.request.GET['start_date']:
            try:
                start_date = datetime.datetime.strptime(self.request.GET['start_date'], '%Y-%m-%d')
                event_list = event_list.filter(event_datetime__gte=start_date)
            except ValueError as e:
                print(f'Can\'t parse date "{self.request.GET["start_date"]}";\n{str(e)}')
        if 'end_date' in self.request.GET.keys() and self.request.GET['end_date']:
            try:
                end_date = datetime.datetime.strptime(self.request.GET['end_date'], '%Y-%m-%d') + \
                           datetime.timedelta(days=1)
                event_list = event_list.filter(event_datetime__lte=end_date)
            except ValueError as e:
                print(f'Can\'t parse date "{self.request.GET["end_date"]}";\n{str(e)}')
        self.response_dict['event_list'] = event_serializers.EventServMiniSerializer(event_list,
                                                                                    many=True).data
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
