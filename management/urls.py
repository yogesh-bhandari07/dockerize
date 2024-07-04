from django.contrib import admin
from django.urls import path
from . import views
from .views import (
    UserView,
    UserRegistrationView,
    VerifyUserEmailView,
    UserLoginView,
    UserProfileView,
    UserChangePasswordView,
    SendPasswordResetEmailView,
    UserPasswordResetView,
)

urlpatterns = [
    path("helath-check", views.healthCheck),
    path("users", UserView.as_view(), name="users"),
    path("users/<int:pk>", UserView.as_view(), name="users"),
    path("user/register", UserRegistrationView.as_view(), name="register"),
    path("user/verify/<uid>/<token>", VerifyUserEmailView.as_view(), name="verify"),
    path("user/login", UserLoginView.as_view(), name="login"),
    path("user/profile", UserProfileView.as_view(), name="profile"),
    path(
        "user/changepassword", UserChangePasswordView.as_view(), name="changepassword"
    ),
    path(
        "user/send-reset-password-email",
        SendPasswordResetEmailView.as_view(),
        name="send-reset-password-email",
    ),
    path(
        "user/reset-password/<uid>/<token>",
        UserPasswordResetView.as_view(),
        name="reset-password",
    ),
]
