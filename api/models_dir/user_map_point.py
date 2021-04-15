import datetime
from django.conf import settings
from django.db import models


class UserMapPoint(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+')
    latitude = models.FloatField()
    longitude = models.FloatField()
    datetime = models.DateTimeField(default=datetime.datetime.now)
