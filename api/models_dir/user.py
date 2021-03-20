from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    color = models.CharField(max_length=10, null=True)
    is_geo_transmitting_permitted = models.BooleanField(default=False)
    is_notifying_permitted = models.BooleanField(default=False)
    image_file = models.ForeignKey(to='File', on_delete=models.SET_NULL, null=True, related_name='+')
    image_file_thumb = models.TextField(null=True)
