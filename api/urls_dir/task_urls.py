from django.urls import path

from api.views_dir.task_views import task_view, task_list_view

urlpatterns = [
    path('note', task_view.TaskView.as_view),
    path('note/list', task_list_view.TaskListView.as_view),
]
