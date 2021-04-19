from rest_framework import serializers

from api.models_dir import budget_category


class BudgetCategoryAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = budget_category.BudgetCategory
        fields = ['name', 'color']


class BudgetCategoryServSerializer(serializers.ModelSerializer):
    class Meta:
        model = budget_category.BudgetCategory
        fields = ['id', 'name', 'color']
