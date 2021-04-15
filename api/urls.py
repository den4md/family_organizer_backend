from django.urls import path, include

urlpatterns = [
    path('', include('api.urls_dir.profile_urls')),
    path('', include('api.urls_dir.group_urls')),
    path('', include('api.urls_dir.file_urls')),
    path('', include('api.urls_dir.task_urls')),
    path('', include('api.urls_dir.map_point_urls')),
    path('', include('api.urls_dir.event_urls')),
    # path('', include('api.urls_dir.budget_urls')),
    # path('', include('api.urls_dir.chat_urls')),
]
