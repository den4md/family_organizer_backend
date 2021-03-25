import datetime

from django.conf import settings
from django.db import models


class File(models.Model):
    name = models.CharField(max_length=50)
    extension = models.CharField(max_length=15, null=True, blank=True)
    size = models.PositiveIntegerField()  # in bytes
    upload_datetime = models.DateTimeField(default=datetime.datetime.now)
    user_uploader = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                      related_name='file_list', blank=True)
    # filepath without ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    file_path = models.CharField(max_length=100, unique=True)
    group = models.ForeignKey(to='Group', null=True, on_delete=models.CASCADE, related_name='file_list', blank=True)
    checksum_md5 = models.CharField(max_length=32)
