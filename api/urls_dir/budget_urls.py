from django.urls import path

from api.views_dir.budget_views import budget_statistics_view, budget_item_list_view, budget_item_view, \
    budget_category_list_view

urlpatterns = [
    path('budget/item', budget_item_view.BudgetItemView.as_view),
    path('budget/item/list', budget_item_list_view.BudgetItemListView.as_view),
    path('budget/categories/list', budget_category_list_view.BudgetCategoryListView.as_view),
    path('budget/statistics', budget_statistics_view.BudgetStatisticsView.as_view),
]
