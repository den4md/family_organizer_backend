from typing import Optional

from django.db.models import Sum

from api.models_dir import group
from api.serializers_dir import budget_item_serializers
from api.views_dir import base_view


class BudgetItemListView(base_view.BaseView):
    url_parameters = ['group_id']

    def handle_get(self) -> Optional[base_view.BaseView]:
        income = base_view.make_float(
            self.dict['group'].budget_item_list.filter(is_income=True).aggregate(Sum('amount'))['amount__sum'])
        consumption = base_view.make_float(
            self.dict['group'].budget_item_list.filter(is_income=False).aggregate(Sum('amount'))['amount__sum'])

        self.response_dict['budget_total'] = income - consumption
        self.response_dict['budget_item_list'] = budget_item_serializers.BudgetItemServSerializer(
            self.dict['group'].budget_item_list, many=True).data

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
