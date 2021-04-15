from __future__ import annotations
from json import JSONDecodeError
from typing import Optional

from django.db.models import Count

from api.helpers import validate_type
from api.models_dir import group, user_map_point, map_point
from api.serializers_dir import map_point_serializers, user_map_point_serializers
from api.views_dir import base_view


class MapPointListView(base_view.BaseView):
    url_parameters = ['group_id']

    def add_user_map_point(self) -> MapPointListView:
        self.response_dict['user_map_point_list'] = user_map_point_serializers.UserMapPointServSerializer(
            user_map_point.UserMapPoint.objects.filter(user__is_geo_transmitting_permitted=True,
                                                       user__group_list=self.dict['group']).order_by(
                'user', '-datetime').distinct('user'), many=True).data
        return self

    def add_map_point(self) -> MapPointListView:
        self.response_dict['map_point_list'] = map_point_serializers.MapPointServMiniSerializer(
            self.dict['group'].map_point_list, many=True).data
        return self

    def add_map_point_event(self) -> MapPointListView:
        self.response_dict['map_point_list'] = map_point_serializers.MapPointServMiniSerializer(
            map_point.MapPoint.objects.filter(group=self.dict['group']).annotate(Count('event_list')).exclude(
                event_list__count=0), many=True).data
        return self

    def handle_get(self) -> Optional[base_view.BaseView]:
        if self.request.body.decode('utf8'):
            try:
                self.deserialize_json_body()
                if 'filter_list' not in self.dict['body_json'].keys() or not validate_type.validate_type(
                        self.dict['body_json']['filter_list'], list):
                    return self.error(f'Can\'t find filter list with values')
                if not self.dict['body_json']['filter_list']:
                    self.add_map_point().add_user_map_point()
                    return self
                if 'point_events' in self.dict['body_json']['filter_list']:
                    self.add_map_point_event()
                if 'points' in self.dict['body_json']['filter_list']:
                    self.add_map_point()
                if 'users' in self.dict['body_json']['filter_list']:
                    self.add_user_map_point()
                if 'all' in self.dict['body_json']['filter_list']:
                    self.add_map_point().add_user_map_point()
            except JSONDecodeError as e:
                self.error(f'Error while deserializing body ({str(e)})')
        else:
            self.add_map_point().add_user_map_point()
        return self

    def chain_get(self):
        self.authorize() \
            .require_url_parameters(self.url_parameters) \
            .get_model_by_id(group.Group, self.request.GET['group_id']) \
            .user_belong_to_group() \
            .request_handlers['GET']['specific'](self)

    request_handlers = {
        "GET": {
            'chain': chain_get,
            'specific': handle_get
        }
    }
