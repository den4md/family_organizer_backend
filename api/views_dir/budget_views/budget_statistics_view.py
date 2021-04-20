import datetime
from typing import Optional, Type, Callable
from django.db import models
from django.db.models import Sum

from api.helpers import write_style_helpers
from api.models_dir import group, budget_category, user
from api.views_dir import base_view


class BudgetStatisticsView(base_view.BaseView):
    url_parameters = ['group_id']

    def filter_by_categories(self):
        self.dict['budget_item_list'] = self.dict['budget_item_list'].filter(
            budget_category_list__id__in=self.dict['body_json']['budget_category_id_list'])

    def filter_by_users(self):
        self.dict['budget_item_list'] = self.dict['budget_item_list'].filter(
            user_payer__id__in=self.dict['body_json']['user_id_list'])

    def check_filter_by_model(self, model: Type[models.Model], filter_method: Callable) -> Optional[base_view.BaseView]:
        model_str = write_style_helpers.camel_case_to_snake_case(model.__name__)
        if f'{model_str}_id_list' not in self.dict['body_json'].keys() or not isinstance(
                self.dict['body_json'][f'{model_str}_id_list'], list):
            return self.error(f'Can\'t find list "{model_str}_id_list" in filters')
        for model_id in self.dict['body_json'][f'{model_str}_id_list']:
            if not self.get_model_by_id(model, model_id):
                return
        filter_method()
        return self

    def handle_get(self) -> Optional[base_view.BaseView]:
        self.dict['budget_item_list'] = self.dict['group'].budget_item_list

        if 'all_budget_categories' not in self.dict['body_json'].keys() or \
                not self.dict['body_json']['all_budget_categories']:
            if not self.check_filter_by_model(budget_category.BudgetCategory, self.filter_by_categories):
                return

        if 'all_users' not in self.dict['body_json'].keys() or \
                not self.dict['body_json']['all_users']:
            if not self.check_filter_by_model(user.User, self.filter_by_users):
                return

        if 'start_date' in self.dict['body_json'].keys() and self.dict['body_json']['start_date']:
            try:
                start_date = datetime.datetime.strptime(self.dict['body_json']['start_date'], '%Y-%m-%d')
                self.dict['budget_item_list'] = self.dict['budget_item_list'].filter(payment_datetime__gte=start_date)
            except ValueError as e:
                return self.error(f'Can\'t parse date "{self.dict["body_json"]["start_date"]}";\n{str(e)}')
        if 'end_date' in self.dict['body_json'].keys() and self.dict['body_json']['end_date']:
            try:
                end_date = datetime.datetime.strptime(self.dict['body_json']['end_date'], '%Y-%m-%d') + \
                           datetime.timedelta(days=1)
                self.dict['budget_item_list'] = self.dict['budget_item_list'].filter(payment_datetime__lte=end_date)
            except ValueError as e:
                return self.error(f'Can\'t parse date "{self.dict["body_json"]["end_date"]}";\n{str(e)}')

        income = base_view.make_float(
            self.dict['budget_item_list'].filter(is_income=True).aggregate(Sum('amount'))['amount__sum'])
        consumption = base_view.make_float(
            self.dict['budget_item_list'].filter(is_income=False).aggregate(Sum('amount'))['amount__sum'])

        self.response_dict['budget_statistics_data'] = {
            'income': income,
            'total': income - consumption,
            'consumption': consumption
        }

        return self

    def chain_get(self):
        self.authorize() \
            .require_url_parameters(self.url_parameters) \
            .get_model_by_id(group.Group, self.request.GET['group_id']) \
            .user_belong_to_group() \
            .deserialize_json_body() \
            .request_handlers['GET']['specific'](self)

    request_handlers = {
        'GET': {
            'chain': chain_get,
            'specific': handle_get
        }
    }
