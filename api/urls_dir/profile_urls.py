from django.urls import path

from api.views_dir.profile_views import sign_up_view, sign_in_view, sign_out_view, profile_view, password_change_view

urlpatterns = [
    path('sign_up', sign_up_view.SignUpView.as_view),
    path('sign_in', sign_in_view.SignInView.as_view),
    path('sign_out', sign_out_view.SignOutView.as_view),
    path('profile', profile_view.ProfileView.as_view),
    path('password_change', password_change_view.PasswordChangeView.as_view)
]
