from django.urls import path, include

urlpatterns = [
    path('', include('api.urls_dir.profile_urls'))
]
