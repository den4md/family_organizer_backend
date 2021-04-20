from typing import Optional

from django.db import IntegrityError
from django.db.models import Count
from rest_framework.exceptions import ValidationError

from api.models_dir import group, user, budget_category, budget_item
from api.serializers_dir import budget_item_serializers, budget_category_serializers
from api.views_dir import base_view


class BudgetItemView(base_view.BaseView):
    url_parameters = ['group_id', 'budget_item_id']

    def collect_budget_category_list(self, target_list: list,
                                     budget_category_list: list) -> Optional[base_view.BaseView]:
        if budget_category_list is not None:
            if not isinstance(budget_category_list, list):
                return self.error(f'Object of "budget_category_list" isn\'t a list')
        else:
            return self

        for budget_category_item in budget_category_list:
            try:
                serializer = budget_category_serializers.BudgetCategoryAppSerializer(data=budget_category_item)
                serializer.is_valid(raise_exception=True)
                budget_category_ = serializer.save(group=self.dict['group'])
            except IntegrityError:
                budget_category_ = budget_category.BudgetCategory.objects.get(name=budget_category_item['name'],
                                                                              group=self.dict['group'])
            except ValidationError as e:
                return self.error(f'Error while validating object: {str(e)}')
            target_list.append(budget_category_)
        return self

    def handle_post(self) -> Optional[base_view.BaseView]:
        if self.dict['body_json']['amount'] <= 0:
            return self.error(f'Can accept only positive amount, not "{str(self.dict["body_json"]["amount"])}"')
        if 'user_payer_id' in self.dict['body_json'].keys() and self.dict['body_json']['user_payer_id'] is not None:
            if not self.get_model_by_id(user.User, self.dict['body_json']['user_payer_id']) or \
                    not self.model_belong_to_group('user'):
                return
        else:
            self.dict['user'] = None

        self.dict['budget_category_list'] = []
        if 'budget_category_list' in self.dict['body_json'].keys():
            if not self.collect_budget_category_list(self.dict['budget_category_list'],
                                                     self.dict['body_json']['budget_category_list']):
                return

        budget_item_ = self.dict['serializer'].save(group=self.dict['group'], user_payer=self.dict['user'])

        for budget_category_ in self.dict['budget_category_list']:
            budget_item_.budget_category_list.add(budget_category_)

        self.response_dict['budget_item_id'] = budget_item_.id
        return self

    def chain_post(self):
        self.authorize() \
            .require_url_parameters([self.url_parameters[0]]) \
            .get_model_by_id(group.Group, self.request.GET['group_id']) \
            .user_belong_to_group() \
            .deserialize_json_body() \
            .body_match_app_serializer(budget_item_serializers.BudgetItemAppSerializer) \
            .app_serializer_validation(budget_item_serializers.BudgetItemAppSerializer) \
            .request_handlers['POST']['specific'](self)

    def handle_get(self) -> Optional[base_view.BaseView]:
        self.response_dict['budget_item_data'] = budget_item_serializers.BudgetItemServSerializer(
            self.dict['budget_item']).data
        return self

    def chain_get(self):
        self.authorize() \
            .require_url_parameters(self.url_parameters) \
            .get_model_by_id(group.Group, self.request.GET['group_id']) \
            .user_belong_to_group() \
            .get_model_by_id(budget_item.BudgetItem, self.request.GET['budget_item_id']) \
            .model_belong_to_group('budget_item') \
            .request_handlers['GET']['specific'](self)

    def clear_unused_budget_categories(self):
        budget_category.BudgetCategory.objects.filter(group=self.dict['group']).annotate(
            Count('budget_item_list')).filter(budget_item_list__count=0).delete()

    def handle_put(self) -> Optional[base_view.BaseView]:
        if 'amount' in self.dict['body_json'].keys() and self.dict['body_json']['amount'] <= 0:
            return self.error(f'Can accept only positive amount, not "{str(self.dict["body_json"]["amount"])}"')
        if 'user_payer_id' in self.dict['body_json'].keys():
            if self.dict['body_json']['user_payer_id'] is not None:
                if not self.get_model_by_id(user.User, self.dict['body_json']['user_payer_id']) or \
                        not self.model_belong_to_group('user'):
                    return
            else:
                self.dict['user'] = None
        if 'budget_category_list' in self.dict['body_json'].keys():
            self.dict['budget_category_list'] = []
            if not self.collect_budget_category_list(self.dict['budget_category_list'],
                                                     self.dict['body_json']['budget_category_list']):
                return

        if 'user_payer_id' in self.dict['body_json'].keys():
            self.dict['budget_item'].user_payer = self.dict['user']

        self.dict['budget_item'].save()

        if 'budget_category_list' in self.dict['body_json'].keys():
            self.dict['budget_item'].budget_category_list.clear()
            for budget_category_ in self.dict['budget_category_list']:
                self.dict['budget_item'].budget_category_list.add(budget_category_)

        self.clear_unused_budget_categories()

        return self

    def chain_put(self):
        self.authorize() \
            .require_url_parameters(self.url_parameters) \
            .get_model_by_id(group.Group, self.request.GET['group_id']) \
            .user_belong_to_group() \
            .get_model_by_id(budget_item.BudgetItem, self.request.GET['budget_item_id']) \
            .model_belong_to_group('budget_item') \
            .deserialize_json_body() \
            .body_match_app_serializer(budget_item_serializers.BudgetItemAppSerializer, required=False) \
            .put_serializer(self.dict['budget_item'], budget_item_serializers.BudgetItemAppSerializer) \
            .request_handlers['PUT']['specific'](self)

    def handle_delete(self) -> Optional[base_view.BaseView]:
        self.dict['budget_item'].delete()
        self.clear_unused_budget_categories()
        return self

    def chain_delete(self):
        self.authorize() \
            .require_url_parameters(self.url_parameters) \
            .get_model_by_id(group.Group, self.request.GET['group_id']) \
            .user_belong_to_group() \
            .get_model_by_id(budget_item.BudgetItem, self.request.GET['budget_item_id']) \
            .model_belong_to_group('budget_item') \
            .request_handlers['DELETE']['specific'](self)

    request_handlers = {
        'POST': {
            'chain': chain_post,
            'specific': handle_post
        },
        'GET': {
            'chain': chain_get,
            'specific': handle_get
        },
        'PUT': {
            'chain': chain_put,
            'specific': handle_put
        },
        'DELETE': {
            'chain': chain_delete,
            'specific': handle_delete
        }
    }
