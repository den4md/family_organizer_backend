from django.db import models


class BudgetCategory(models.Model):
    name = models.CharField(max_length=20, unique=True)
    color = models.CharField(max_length=10)
