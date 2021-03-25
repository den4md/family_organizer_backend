from django.urls import path

from api.views_dir.file_views import file_view, file_info_view, file_list_view

urlpatterns = [
    path('file', file_view.FileView.as_view),
    path('file/info', file_info_view.FileInfoView.as_view),
    path('file/list', file_list_view.FileListView.as_view),
]
