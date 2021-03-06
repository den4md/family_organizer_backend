import datetime

from django.conf import settings
from django.db import models


class BaseTask(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=75)
    description = models.TextField(null=True, blank=True)
    file_list = models.ManyToManyField(to='File', related_name='+')
    deadline_datetime = models.DateTimeField(null=True, blank=True)
    user_responsible_list = models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='+')
    status = models.CharField(max_length=20, null=True, blank=True)
    user_creator = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='+', null=True,
                                     on_delete=models.SET_NULL, blank=True)
    create_date = models.DateField(default=datetime.datetime.now)
