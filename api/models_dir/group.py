from django.conf import settings
from django.utils import timezone
from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=75)
    create_date = models.DateField(default=timezone.now)
    invite_id = models.CharField(max_length=75, null=True, unique=True)
    user_creator = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                     related_name='+')
    user_member_list = models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='group_list')
    image_file = models.ForeignKey(to='File', on_delete=models.SET_NULL, null=True, related_name='+')
    image_file_thumb = models.TextField(null=True)
