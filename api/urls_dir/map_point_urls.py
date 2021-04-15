from django.urls import path

from api.views_dir.map_point_views import map_point_view, user_map_point_view, map_point_list_view

urlpatterns = [
    path('map_point', map_point_view.MapPointView.as_view),
    path('user_map_point', user_map_point_view.UserMapPointView.as_view),
    path('map_point/list', map_point_list_view.MapPointListView.as_view),
]
