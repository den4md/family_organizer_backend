from django.urls import path

from api.views_dir.chat_views import chat_list_view, chat_view, chat_message_list_view, chat_message_view, \
    chat_file_list_view, chat_file_view

urlpatterns = [
    path('chat/list', chat_list_view.ChatListView.as_view),
    path('chat', chat_view.ChatView.as_view),
    path('chat/message/list', chat_message_list_view.ChatMessageListView.as_view),
    path('chat/message', chat_message_view.ChatMessageView.as_view),
    path('chat/file/list', chat_file_list_view.ChatFileListView.as_view),
    path('chat/file', chat_file_view.ChatFileView.as_view),
]
