from django.urls import path
from django.contrib.auth.views import LogoutView
from users.views import (
    UserSignupView,
    UserLoginView,
    UserDetailView,
)

urlpatterns = [
    path("signup/", UserSignupView.as_view(), name="user-signup"),
    path("login/", UserLoginView.as_view(), name="user-login"),
    path("logout/", LogoutView.as_view(), name="user-logout"),
    path("profile/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
]
