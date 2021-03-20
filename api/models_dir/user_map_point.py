from django.conf import settings
from django.db import models
from django.utils import timezone


class UserMapPoint(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+')
    longitude = models.FloatField()
    latitude = models.FloatField()
    datetime = models.DateTimeField(default=timezone.now)
