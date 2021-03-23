from django.db import models


class BudgetCategory(models.Model):
    name = models.CharField(max_length=20)
    color = models.CharField(max_length=10)
    group = models.ForeignKey(to='Group', on_delete=models.CASCADE, related_name='budget_item_category_list')

    class Meta:
        unique_together = ['name', 'group']
