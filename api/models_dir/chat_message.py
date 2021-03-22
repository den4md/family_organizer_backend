from django.conf import settings
from django.db import models
from django.utils import timezone


class ChatMessage(models.Model):
    is_text = models.BooleanField()
    text = models.TextField(null=True, blank=True)
    file = models.ForeignKey(to='File', null=True, on_delete=models.CASCADE, related_name='+', blank=True)
    user_sender = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='+', null=True,
                                    on_delete=models.SET_NULL, blank=True)
    send_datetime = models.DateTimeField(default=timezone.now)
    chat = models.ForeignKey(to='Chat', on_delete=models.CASCADE, related_name='chat_message_list')
