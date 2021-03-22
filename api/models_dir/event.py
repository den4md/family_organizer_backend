from django.conf import settings
from django.db import models
from django.utils import timezone


class Event(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    event_datetime = models.DateTimeField()
    file_list = models.ManyToManyField(to='File', related_name='+')
    map_point = models.ForeignKey(to='MapPoint', null=True, on_delete=models.CASCADE, related_name='event_list',
                                  blank=True)
    notify_datetime = models.DateTimeField(null=True, blank=True)
    create_date = models.DateField(default=timezone.now)
    user_creator = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='+', null=True,
                                     on_delete=models.SET_NULL, blank=True)
    group = models.ForeignKey(to='Group', on_delete=models.CASCADE, related_name='event_list')
