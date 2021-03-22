from django.contrib import admin
from django.urls import path, include

from api.views_dir import view_404, view_400

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls'))
]

handler404 = view_404.View404.as_view
handler400 = view_400.View400.as_view
