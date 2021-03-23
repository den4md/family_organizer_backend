from django.conf import settings
from django.db import models


class ChatUserSettings(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+')
    chat = models.ForeignKey(to='Chat', on_delete=models.CASCADE, related_name='chat_user_settings')
    number_of_unread_messages = models.IntegerField(default=0)
    is_notifying = models.BooleanField(default=True)

    class Meta:
        unique_together = ['user', 'chat']
