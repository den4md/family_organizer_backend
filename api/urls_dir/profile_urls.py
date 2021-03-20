from django.urls import path

from api.views_dir.profile_views import sign_up_view

urlpatterns = [
    path('sign_up', sign_up_view.SignUpView.as_view)
]
