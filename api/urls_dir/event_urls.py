from django.urls import path

from api.views_dir.event_views import event_view, event_list_view

urlpatterns = [
    path('event', event_view.EventView.as_view),
    path('event/list', event_list_view.EventListView.as_view),
]
