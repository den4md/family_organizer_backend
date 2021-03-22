from django.conf import settings
from django.utils import timezone
from django.db import models


class File(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=5, null=True, blank=True)
    size = models.PositiveIntegerField()  # in bytes
    upload_datetime = models.DateTimeField(default=timezone.now)
    user_uploader = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                      related_name='file_list', blank=True)
    # filepath without ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    file_path = models.CharField(max_length=100, unique=True)
    group = models.ForeignKey(to='Group', null=True, on_delete=models.CASCADE, related_name='file_list', blank=True)
    # TODO add unique checksum to exclude appearing of duplicates
