from rest_framework import serializers

from api.models_dir import budget_item
from api.serializers_dir import base_app_serializer, user_serializers, budget_category_serializers
from api.serializers_dir.custom_fields import string_datetime_field


class BudgetItemAppSerializer(base_app_serializer.BaseAppSerializer):
    class Meta:
        model = budget_item.BudgetItem
        required_fields = {'is_income', 'amount'}
        non_required_fields = {'name', 'payment_datetime', 'user_payer_id', 'budget_category_list'}
        possible_fields = required_fields | non_required_fields
        non_serialized_fields = {'user_payer_id', 'budget_category_list'}
        fields = list(possible_fields - non_serialized_fields)


class BudgetItemServSerializer(serializers.ModelSerializer):
    payment_datetime = string_datetime_field.StringDatetimeField(read_only=True)
    user_payer = user_serializers.UserServMiniSerializer(read_only=True)
    budget_category_list = budget_category_serializers.BudgetCategoryServSerializer(many=True, read_only=True)

    class Meta:
        model = budget_item.BudgetItem
        fields = ['id', 'is_income', 'amount', 'name', 'payment_datetime', 'user_payer', 'budget_category_list']
