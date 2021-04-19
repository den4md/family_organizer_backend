from __future__ import annotations

from typing import Optional

from django.db.models import Count

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

    def add_all(self) -> MapPointListView:
        return self.add_user_map_point().add_map_point()

    # noinspection PyArgumentList
    def handle_get(self) -> Optional[base_view.BaseView]:
        filtered = False

        for get_key in self.filter_url_parameters.keys():
            if get_key in self.request.GET.keys() and self.request.GET[get_key].lower() == 'true':
                filtered = True
                self.filter_url_parameters[get_key](self)

        if not filtered:
            self.add_all()
        return self

    def chain_get(self):
        self.authorize() \
            .require_url_parameters(self.url_parameters) \
            .get_model_by_id(group.Group, self.request.GET['group_id']) \
            .user_belong_to_group() \
            .request_handlers['GET']['specific'](self)

    filter_url_parameters = {
        'point_events': add_map_point_event,
        'points': add_map_point,
        'users': add_user_map_point,
        'all': add_all
    }

    request_handlers = {
        "GET": {
            'chain': chain_get,
            'specific': handle_get
        }
    }
