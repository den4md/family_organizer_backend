import datetime

from django.conf import settings
from django.db import models


class BudgetItem(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    is_income = models.BooleanField()
    payment_datetime = models.DateTimeField(default=datetime.datetime.now)
    user_payer = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='+', null=True,
                                   on_delete=models.SET_NULL, blank=True)
    budget_category_list = models.ManyToManyField(to='BudgetCategory', related_name='budget_item_list')
    group = models.ForeignKey(to='Group', on_delete=models.CASCADE, related_name='budget_item_list')
