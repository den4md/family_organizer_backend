from django.conf import settings
from django.db import models
from django.utils import timezone


class MapPoint(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)
    image_file = models.ForeignKey(to='File', null=True, on_delete=models.SET_NULL, related_name='+')
    longitude = models.FloatField()
    latitude = models.FloatField()
    create_date = models.DateField(default=timezone.now)
    user_creator = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='+', null=True,
                                     on_delete=models.SET_NULL)
    group = models.ForeignKey(to='Group', on_delete=models.CASCADE, related_name='map_point_list')
