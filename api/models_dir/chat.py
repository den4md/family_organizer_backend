from django.conf import settings
from django.db import models


class Chat(models.Model):
    user_member_list = models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='+', through='ChatUserSettings')
    group = models.ForeignKey(to='Group', on_delete=models.CASCADE, related_name='chat_list')
